import ray
from ray.tune.search import optuna
import optuna


def get_search_space(input_dim):
    # Note: epochs is controlled by the frontend form, not the search space
    return {
        "model": {
            "input_dim": input_dim,
            "output_dim": 1,
            "hidden_dim": ray.tune.choice([2**x for x in range(4, 9)]),
            "n_layers": ray.tune.choice(range(2, 6)),
            "drop_prob": ray.tune.quniform(0.1, 0.5, 0.05),
        },
        "criterion": {},
        "optimizer": {"lr": 1e-3},
        "scheduler": {
            "mode": "min",
            "factor": ray.tune.quniform(0.5, 0.75, 0.05),
            "patience": ray.tune.choice(range(5, 8)),
            "min_lr": 1e-8,
        },
    }
