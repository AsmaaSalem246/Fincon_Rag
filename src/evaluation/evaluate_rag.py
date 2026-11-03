
import os
import json
import asyncio
from pathlib import Path
import litellm
from dotenv import load_dotenv
from groq import Groq
from ragas.llms import llm_factory
from ragas.embeddings import embedding_factory
from openai import AsyncOpenAI
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

from src.config import settings
from src.generation.chain import FinConRAGPipeline


# =====================================================
# 1. Load Environment Variables
# =====================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )


# =====================================================
# 2. Initialize Groq Evaluator LLM
# =====================================================
evaluator_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=120.0,
    max_retries=3
)

evaluator_llm = llm_factory(
    model="openai/gpt-oss-120b",
    provider="openai",
    client=evaluator_client,
    adapter="instructor",
    temperature=0,
    max_completion_tokens=8192,
    reasoning_effort="low"
    
)

# =====================================================
# 3. Initialize Evaluator Embeddings
# =====================================================

evaluator_embeddings = embedding_factory(
    provider="huggingface",
    model=settings.EMBEDDING_MODEL_NAME,
)


# =====================================================
# 4. Initialize RAGAS Metrics
# =====================================================

faithfulness_metric = Faithfulness(
    llm=evaluator_llm
)

answer_relevancy_metric = AnswerRelevancy(
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)

context_precision_metric = ContextPrecision(
    llm=evaluator_llm
)

context_recall_metric = ContextRecall(
    llm=evaluator_llm
)


# =====================================================
# 5. Helper Functions
# =====================================================

def get_score(result):

    return round(float(result.value), 4)


def get_reason(result):

    return getattr(result, "reason", None)


def calculate_average(results, metric_name):

    scores = [
        item[metric_name]
        for item in results
        if item.get(metric_name) is not None
    ]

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 4)


# =====================================================
# 6. Main Evaluation Function
# =====================================================

async def evaluate_rag(
    golden_path=None,
    output_path=None
):

    if golden_path is None:
        golden_path = (
            ROOT_DIR / "data" / "golden_eval_set.json"
        )

    if output_path is None:
        output_path = (
            ROOT_DIR / "data" / "ragas_evaluation_results.json"
        )

    golden_path = Path(golden_path)
    output_path = Path(output_path)

    # -----------------------------------------
    # Load Golden Evaluation Dataset
    # -----------------------------------------

    if not golden_path.exists():
        raise FileNotFoundError(
            f"Golden dataset not found: {golden_path}"
        )

    with open(golden_path, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    if not golden_data:
        raise ValueError("Golden dataset is empty.")

    # -----------------------------------------
    # Initialize RAG Pipeline
    # -----------------------------------------

    pipeline = FinConRAGPipeline()

    results = []

    total_queries = len(golden_data)

    print("\n========================================")
    print("       RAGAS EVALUATION STARTED")
    print("========================================")

    print(f"Total Queries: {total_queries}")
    print("Evaluator: Groq GPT-OSS 120B")

    # -----------------------------------------
    # Process Each Question
    # -----------------------------------------

    for idx, item in enumerate(golden_data, start=1):

        query = item["query"]

        reference = item.get(
            "ground_truth_answer", ""
        )

        print(f"\n[{idx}/{total_queries}] Evaluating:")
        print(query)

        try:

            # =================================
            # A. Run the RAG Pipeline
            # =================================

            res = pipeline.run(
                query=query,
                top_k_rerank=3
            )

            generated_answer = res.get(
                "answer", ""
            )

            retrieved_child_chunks = res.get(
                "retrieved_child_chunks", []
            )

            # Extract Retrieved Contexts

            retrieved_contexts = [
                chunk.get("text", "")
                for chunk in retrieved_child_chunks
                if chunk.get("text")
            ]

            # =================================
            # B. Faithfulness
            # =================================

            faithfulness_score = None
            faithfulness_reason = None

            if generated_answer and retrieved_contexts:

                result = await faithfulness_metric.ascore(
                    user_input=query,
                    response=generated_answer,
                    retrieved_contexts=retrieved_contexts
                )

                faithfulness_score = get_score(result)
                faithfulness_reason = get_reason(result)

            # =================================
            # C. Answer Relevancy
            # =================================

            answer_relevancy_score = None
            answer_relevancy_reason = None

            if generated_answer:

                result = await answer_relevancy_metric.ascore(
                    user_input=query,
                    response=generated_answer
                )

                answer_relevancy_score = get_score(result)
                answer_relevancy_reason = get_reason(result)

            # =================================
            # D. Context Precision
            # =================================

            context_precision_score = None
            context_precision_reason = None

            if reference and retrieved_contexts:

                result = await context_precision_metric.ascore(
                    user_input=query,
                    retrieved_contexts=retrieved_contexts,
                    reference=reference
                )

                context_precision_score = get_score(result)
                context_precision_reason = get_reason(result)

            # =================================
            # E. Context Recall
            # =================================

            context_recall_score = None
            context_recall_reason = None

            if reference and retrieved_contexts:

                result = await context_recall_metric.ascore(
                    user_input=query,
                    retrieved_contexts=retrieved_contexts,
                    reference=reference
                )

                context_recall_score = get_score(result)
                context_recall_reason = get_reason(result)

            # =================================
            # F. Store Individual Results
            # =================================

            query_result = {

                "query": query,

                "ground_truth": reference,

                "generated_answer": generated_answer,

                "retrieved_contexts": retrieved_contexts,

                "faithfulness": faithfulness_score,

                "faithfulness_reason": faithfulness_reason,

                "answer_relevancy": answer_relevancy_score,

                "answer_relevancy_reason": answer_relevancy_reason,

                "context_precision": context_precision_score,

                "context_precision_reason": context_precision_reason,

                "context_recall": context_recall_score,

                "context_recall_reason": context_recall_reason,

            }

            results.append(query_result)

            print("\nQuery Evaluation Results:")

            for metric in [
                "faithfulness",
                "answer_relevancy",
                "context_precision",
                "context_recall"
            ]:

                print(
                    f"{metric}: {query_result[metric]}"
                )

        except Exception as e:

            print(f"Error evaluating query: {e}")

            results.append({
                "query": query,
                "error": str(e)
            })

        # Avoid sending requests too quickly

        await asyncio.sleep(0.5)

    # =================================================
    # 7. Calculate Overall Scores
    # =================================================

    summary = {

        "total_test_queries": total_queries,

        "successfully_evaluated": sum(
            1 for item in results
            if "error" not in item
        ),

        "average_faithfulness": calculate_average(
            results, "faithfulness"
        ),

        "average_answer_relevancy": calculate_average(
            results, "answer_relevancy"
        ),

        "average_context_precision": calculate_average(
            results, "context_precision"
        ),

        "average_context_recall": calculate_average(
            results, "context_recall"
        ),

    }

    # =================================================
    # 8. Save Evaluation Report
    # =================================================

    report = {

        "evaluator_model": "openai/gpt-oss-120b",

        "summary": summary,

        "details": results

    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    # =================================================
    # 9. Print Final Report
    # =================================================

    print("\n========================================")
    print("       RAGAS EVALUATION REPORT")
    print("========================================")

    print(
        f"Total Queries: {summary['total_test_queries']}"
    )

    print(
        f"Successfully Evaluated: "
        f"{summary['successfully_evaluated']}"
    )

    print("----------------------------------------")

    print(
        f"Faithfulness: "
        f"{summary['average_faithfulness']:.4f}"
    )

    print(
        f"Answer Relevancy: "
        f"{summary['average_answer_relevancy']:.4f}"
    )

    print(
        f"Context Precision: "
        f"{summary['average_context_precision']:.4f}"
    )

    print(
        f"Context Recall: "
        f"{summary['average_context_recall']:.4f}"
    )

    print("----------------------------------------")

    print(f"Report saved to: {output_path}")

    print("========================================")

    return report


# =====================================================
# 10. Run Evaluation
# =====================================================

if __name__ == "__main__":

    asyncio.run(evaluate_rag())
