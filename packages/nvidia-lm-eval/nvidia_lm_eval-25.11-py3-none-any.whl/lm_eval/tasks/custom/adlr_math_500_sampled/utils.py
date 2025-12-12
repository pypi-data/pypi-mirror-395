import itertools

import numpy as np
from lm_eval.tasks.custom.adlr_math_500_sampled.few_shot_examples import examples_map
from math_verify import parse


def doc_to_text(doc: dict) -> str:
    return "Problem:" + "\n" + doc["problem"] + "\n\n" + "Solution:"


def standard_math_fewshot_samples() -> list[dict]:
    return examples_map["math_standard_few_shot"]


def detailed_math_fewshot_samples() -> list[dict]:
    return examples_map["math_text_detailed"]


def standard_gsm8k_fewshot_samples() -> list[dict]:
    return examples_map["gsm8k_standard_few_shot"]


def detailed_gsm8k_fewshot_samples() -> list[dict]:
    return examples_map["gsm8k_detailed_few_shot"]


def doc_to_target(doc: dict) -> str:
    for k in ["solution", "answer", "reference_solution", "expected_answer"]:
        if k in doc:
            return doc[k]
    return parse(doc["solution"])[1]


def estimate_pass_at_k(num_samples, num_correct, k):
    """Estimates pass@k of each problem and returns them in an array."""

    def estimator(n: int, c: int, k: int) -> float:
        """Calculates 1 - comb(n - c, k) / comb(n, k)."""
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )


def estimate_pass_at_k_dynamic(doc: dict, results: list[list[dict]]) -> dict:
    """Pass@k estimation function with dynamic K sweep (powers of 2 up to N)."""
    result_list = results[0]  # filter_fn results
    passed = [r["passed"] for r in result_list]
    total = len(passed)
    correct = sum(passed)

    N = total
    Ks = set([2**x for x in range(0, int(np.log2(N)) + 1)] + [N])
    pass_at_k_results = {}
    for k in Ks:
        pass_at_k_results[f"pass@{k}[{N}]"] = estimate_pass_at_k([total], [correct], k)[
            0
        ]
    return pass_at_k_results
