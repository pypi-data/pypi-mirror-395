# Frames

The task involves answering questions based on a prompt and a set of relevant Wikipedia articles. 

We support 4 evaluation strategies:

- Naive (task: `frames_naive`): uses the prompt as input without additional context
- Naive with links (task: `frames_naive_with_links`): provides the prompt and relevant Wikipedia article links
- Oracle with processed wikipedia articles (task: `frames_oracle`): provides the prompt and relevant text from curated and processed Wikipedia articles (from "parasail-ai/frames-benchmark-wikipedia")
- Oracle with raw wikipedia articles (task: `frames_oracle_raw`): provides the prompt and raw text extracted from Wikipedia articles, retrieved from Wikipedia links and parsed from HTML using BeautifulSoup HTML parser, which may include large unstructured content

## Resources

1. Paper: https://arxiv.org/pdf/2409.12941
2. Dataset: https://huggingface.co/datasets/google/frames-benchmark
3. Frames benchmark wikipedia: https://huggingface.co/datasets/parasail-ai/frames-benchmark-wikipedia
4. Implementation based on: https://github.com/codelion/optillm/blob/main/scripts/eval_frames_benchmark.py (extended with different evaluation strategies)
5. Processed wikipedia articles: https://huggingface.co/datasets/parasail-ai/frames-benchmark-wikipedia
