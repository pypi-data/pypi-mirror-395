import ray
from ray.tune.search import optuna
import optuna


def get_search_space(input_dim):
    """
    Returns the default Transformer search space configuration.
    Note: epochs is set from cfg.tune.epochs, not the search space template.
    """
    return {
        "model": {
            "input_dim": input_dim,
            "output_dim": 1,
            "hidden_dim": ray.tune.choice([2**xx for xx in range(4, 9)]),
            "n_layers": ray.tune.choice(range(2, 6)),
            "head_div": ray.tune.choice([2**xx for xx in range(1, 4)]),
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
