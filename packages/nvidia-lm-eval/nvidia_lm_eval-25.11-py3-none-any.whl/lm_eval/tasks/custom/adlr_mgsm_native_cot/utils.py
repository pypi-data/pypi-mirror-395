from lm_eval.api.metrics import exact_match_hf_evaluate


def process_results_exact_match_answer_number_or_passed(doc, results):
    result = results[0]
    if (
        # Such an answer comes from the symbolic match filter
        isinstance(result, list)
        and len(result) > 0
        and isinstance(result[0], dict)
        and "passed" in result[0].keys()
    ):
        score = sum(r["passed"] for r in result) / len(result)  # batch dim. agg.
        return {
            "exact_match": score,
        }
    else:
        # Process gold as per doc_to_target template in the task config
        gold = str(doc["answer_number"])
        return exact_match_hf_evaluate(
            references=[gold],
            predictions=[result],
            ignore_case=True,
            ignore_punctuation=True,
        )
