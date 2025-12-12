from spotoptim.sampling.mm import mm_improvement
import numpy as np


def mo_mm_desirability_function(
    x, models, X_base, J_base, d_base, phi_base, D_overall, mm_objective=True
):
    """
    Calculates the negative combined desirability for a candidate point x. Can be used by the mo_mm_desirability_optimizer.
    For each objective, a model is used to predict the objective value at x. If mm_objective is True, the Morris-Mitchell improvement is also calculated and included as an additional objective.
    The combined desirability, which uses the predictions from the models and optionally the Morris-Mitchell improvement, is then computed using the provided DOverall object.

    Args:
        x (np.ndarray):
            Candidate point (1D array).
        models (list):
            List of trained models. One model per objective.
        X_base (np.ndarray):
            Existing design points. Used for computing Morris-Mitchell improvement.
        J_base (np.ndarray):
            Multiplicities of distances for X_base. Used for Morris-Mitchell improvement.
        d_base (np.ndarray):
            Unique distances for X_base. Used for Morris-Mitchell improvement.
        phi_base (float):
            Base Morris-Mitchell metric for X_base. Used for Morris-Mitchell improvement.
        D_overall (DOverall):
            The overall desirability function. Must include desirability functions for each objective and optionally for Morris-Mitchell.
        mm_objective (bool):
            Whether to include space-filling improvement as an objective. Defaults to True.

    Returns:
        float: Negative geometric mean of desirabilities (for minimization).
        list: List of individual objective values.

    Examples:
        >>> from spotoptim.mo import mo_mm_desirability_function
        >>> from spotoptim.desirability import DOverall, DMin, DMax
        >>> import numpy as np
        >>> from spotoptim.function.mo import mo_conv2_max
        >>> # X_base in the range [0,1]
        >>> X_base = np.random.rand(500, 2)
        >>> y = mo_conv2_max(X_base)
        >>> models = []
        >>> for i in range(y.shape[1]):
        ...     model = RandomForestRegressor(n_estimators=100, random_state=42)
        ...     model.fit(X_base, y[:, i])
        ...     models.append(model)
        >>> # calculate base Morris-Mitchell stats
        >>> phi_base, J_base, d_base = mmphi_intensive(X_base, q=2, p=2)
        >>> d_funcs = []
        >>> for i in range(y.shape[1]):
        ...     d_func = DMax(low=np.min(y[:, i]), high=np.max(y[:, i]))
        ...     d_funcs.append(d_func)
        >>> D_overall = DOverall(*d_funcs)
        >>> neg_D, objectives = mo_mm_desirability_function(x_test, models, X_base, J_base, d_base, phi_base, D_overall, mm_objective=False)
        >>> print(f"Negative Desirability: {neg_D}")
        >>> print(f"Objectives: {objectives}")
    """
    # 1. Predict for all models
    x_reshaped = x.reshape(1, -1)
    predictions = [model.predict(x_reshaped)[0] for model in models]

    # 2. Compute y_mm (Space-filling improvement) if requested
    if mm_objective:
        y_mm = mm_improvement(x, X_base, phi_base, J_base, d_base)
        predictions.append(y_mm)

    # 3. Calculate combined desirability
    D = D_overall.predict(predictions)

    # Ensure D is a scalar
    if isinstance(D, np.ndarray):
        D = D.item()

    return -D, predictions
