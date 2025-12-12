# Reward bench task

## Links

- HF dataset: https://huggingface.co/datasets/allenai/reward-bench

- Leaderboard: https://huggingface.co/spaces/allenai/reward-bench

- Paper: https://arxiv.org/abs/2403.13787

- GH: https://github.com/allenai/reward-bench

## Notes

- Currently supporting Nemo models with chat template applied by default (please see task.py)

## Results

- Model = "Nemotron-4-340B-Reward", num_fewshot = 0, batch_size = 1: 
    - reward bench score: 0.92261 
    - stderr: 0.00489
