import ray


def get_search_space(input_dim):
    return {
        "window_inc": ray.tune.quniform(2, 10, 1),
        "alphabet_size": ray.tune.quniform(2, 10, 1),
        "feature_selection": ray.tune.choice(["chi2", "none", "random"]),
    }
