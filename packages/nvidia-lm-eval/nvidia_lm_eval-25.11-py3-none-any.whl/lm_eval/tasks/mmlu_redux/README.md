# MMLU-Redux

MMLU-Redux is a subset of 3,000 manually re-annotated questions across 30 MMLU subjects. See the [Huggingface dataset](https://huggingface.co/datasets/edinburgh-dawg/mmlu-redux).

We adopt generation-based evaluation protocol. We utilize the Zero-Eval prompt format [(Lin, 2024)](https://github.com/WildEval/ZeroEval/tree/main), with a zero-shot setting in mind, as in the DeepSeek-v3 paper.

## Paper

Title: `Are We Done with MMLU?`

Abstract: `Maybe not. We identify and analyse errors in the popular Massive Multitask Language Understanding (MMLU) benchmark. Even though MMLU is widely adopted, our analysis demonstrates numerous ground truth errors that obscure the true capabilities of LLMs. For example, we find that 57% of the analysed questions in the Virology subset contain errors. To address this issue, we introduce a comprehensive framework for identifying dataset errors using a novel error annotation protocol. Then, we create MMLU-Redux, which is a subset of 5,700 manually re-annotated questions across all 57 MMLU subjects. We estimate that 6.49% of MMLU questions contain errors. Using MMLU-Redux, we demonstrate significant discrepancies with the model performance metrics that were originally reported. Our results strongly advocate for revising MMLU's error-ridden questions to enhance its future utility and reliability as a benchmark.`

Homepage: https://github.com/aryopg/mmlu-redux

### Citation:

```bibtex
@article{gema2025mmlu,
    title={Are We Done with MMLU?},
    author={Aryo Pradipta Gema and Joshua Ong Jun Leang and Giwon Hong and Alessio Devoto and Alberto Carlo Maria Mancino and Rohit Saxena and Xuanli He and Yu Zhao and Xiaotang Du and Mohammad Reza Ghasemi Madani and Claire Barale and Robert McHardy and Joshua Harris and Jean Kaddour and Emile van Krieken and Pasquale Minervini},
    journal={arXiv preprint arXiv:2406.04127},
    year={2024},
}
```

## Task Validity Checklist

The checklist is the following:

For adding novel benchmarks/datasets to the library:
* [x] Is the task an existing benchmark in the literature?
  * [x] Have you referenced the original paper that introduced the task?
  * [x] If yes, does the original paper provide a reference implementation? If so, have you checked against the reference implementation and documented how to run such a test?


If other tasks on this dataset are already supported:
* [x] Is the "Main" variant of this task clearly denoted?
* [x] Have you provided a short sentence in a README on what each new variant adds / evaluates?
* [x] Have you noted which, if any, published evaluation setups are matched by this variant?