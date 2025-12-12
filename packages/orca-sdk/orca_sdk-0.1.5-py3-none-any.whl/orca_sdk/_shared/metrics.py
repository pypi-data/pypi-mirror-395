"""
This module contains metrics for usage with the Hugging Face Trainer.

IMPORTANT:
- This is a shared file between OrcaLib and the OrcaSDK.
- Please ensure that it does not have any dependencies on the OrcaLib code.
- Make sure to edit this file in orcalib/shared and NOT in orca_sdk, since it will be overwritten there.

"""

from dataclasses import dataclass
from typing import Any, Literal, Sequence, TypedDict, cast

import numpy as np
import sklearn.metrics
from numpy.typing import NDArray


# we don't want to depend on scipy or torch in orca_sdk
def softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = logits - np.max(logits, axis=axis, keepdims=True)
    exps = np.exp(shifted)
    return exps / np.sum(exps, axis=axis, keepdims=True)


# We don't want to depend on transformers just for the eval_pred type in orca_sdk
def transform_eval_pred(eval_pred: Any) -> tuple[NDArray, NDArray[np.float32]]:
    # convert results from Trainer compute_metrics param for use in calculate_classification_metrics
    logits, references = eval_pred  # transformers.trainer_utils.EvalPrediction
    if isinstance(logits, tuple):
        logits = logits[0]
    if not isinstance(logits, np.ndarray):
        raise ValueError("Logits must be a numpy array")
    if not isinstance(references, np.ndarray):
        raise ValueError(
            "Multiple label columns found, use the `label_names` training argument to specify which one to use"
        )

    return (references, logits)


def convert_to_float32_array(
    data: (
        Sequence[float | None]
        | NDArray[np.float32]
        | Sequence[Sequence[float]]
        | Sequence[NDArray[np.float32]]
        | NDArray[np.float32]
    ),
) -> NDArray[np.float32]:
    """
    Convert a list or array that may contain None values to a float32 numpy array.
    None values are converted to NaN.

    Args:
        data: Input data that may contain None values

    Returns:
        A float32 numpy array with None values converted to NaN
    """
    array = np.array(data)
    # Convert None values to NaN to handle missing values
    if array.dtype == object:

        def convert_value(x):
            return np.nan if x is None else float(x)

        array = np.vectorize(convert_value, otypes=[np.float32])(array)
    else:
        array = np.asarray(array, dtype=np.float32)
    return cast(NDArray[np.float32], array)


def calculate_anomaly_score_stats(
    anomaly_scores: NDArray[np.float32] | Sequence[float] | None,
) -> tuple[float | None, float | None, float | None]:
    """
    Calculate statistics (mean, median, variance) for anomaly scores.

    Args:
        anomaly_scores: Anomaly scores as a list, numpy array, or None

    Returns:
        A tuple of (mean, median, variance). All values are None if anomaly_scores is None.
    """
    if anomaly_scores is None:
        return (None, None, None)

    # Convert to numpy array if needed
    if isinstance(anomaly_scores, list):
        anomalies = np.array(anomaly_scores, dtype=np.float32)
    else:
        anomalies = anomaly_scores

    return (
        float(np.mean(anomalies)),
        float(np.median(anomalies)),
        float(np.var(anomalies)),
    )


class PRCurve(TypedDict):
    thresholds: list[float]
    precisions: list[float]
    recalls: list[float]


def calculate_pr_curve(
    references: NDArray[np.int64],
    probabilities: NDArray[np.float32],
    max_length: int = 100,
) -> PRCurve:
    if probabilities.ndim == 1:
        probabilities_slice = probabilities
    elif probabilities.ndim == 2:
        probabilities_slice = probabilities[:, 1]
    else:
        raise ValueError("Probabilities must be 1 or 2 dimensional")

    if len(probabilities_slice) != len(references):
        raise ValueError("Probabilities and references must have the same length")

    precisions, recalls, thresholds = sklearn.metrics.precision_recall_curve(references, probabilities_slice)

    # Convert all arrays to float32 immediately after getting them
    precisions = precisions.astype(np.float32)
    recalls = recalls.astype(np.float32)
    thresholds = thresholds.astype(np.float32)

    # Concatenate with 0 to include the lowest threshold
    thresholds = np.concatenate(([0], thresholds))

    # Sort by threshold
    sorted_indices = np.argsort(thresholds)
    thresholds = thresholds[sorted_indices]
    precisions = precisions[sorted_indices]
    recalls = recalls[sorted_indices]

    if len(precisions) > max_length:
        new_thresholds = np.linspace(0, 1, max_length, dtype=np.float32)
        new_precisions = np.interp(new_thresholds, thresholds, precisions)
        new_recalls = np.interp(new_thresholds, thresholds, recalls)
        thresholds = new_thresholds
        precisions = new_precisions
        recalls = new_recalls

    return PRCurve(
        thresholds=cast(list[float], thresholds.tolist()),
        precisions=cast(list[float], precisions.tolist()),
        recalls=cast(list[float], recalls.tolist()),
    )


class ROCCurve(TypedDict):
    thresholds: list[float]
    false_positive_rates: list[float]
    true_positive_rates: list[float]


def calculate_roc_curve(
    references: NDArray[np.int64],
    probabilities: NDArray[np.float32],
    max_length: int = 100,
) -> ROCCurve:
    if probabilities.ndim == 1:
        probabilities_slice = probabilities
    elif probabilities.ndim == 2:
        probabilities_slice = probabilities[:, 1]
    else:
        raise ValueError("Probabilities must be 1 or 2 dimensional")

    if len(probabilities_slice) != len(references):
        raise ValueError("Probabilities and references must have the same length")

    # Convert probabilities to float32 before calling sklearn_roc_curve
    probabilities_slice = probabilities_slice.astype(np.float32)
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(references, probabilities_slice)

    # Convert all arrays to float32 immediately after getting them
    fpr = fpr.astype(np.float32)
    tpr = tpr.astype(np.float32)
    thresholds = thresholds.astype(np.float32)

    # We set the first threshold to 1.0 instead of inf for reasonable values in interpolation
    thresholds[0] = 1.0

    # Sort by threshold
    sorted_indices = np.argsort(thresholds)
    thresholds = thresholds[sorted_indices]
    fpr = fpr[sorted_indices]
    tpr = tpr[sorted_indices]

    if len(fpr) > max_length:
        new_thresholds = np.linspace(0, 1, max_length, dtype=np.float32)
        new_fpr = np.interp(new_thresholds, thresholds, fpr)
        new_tpr = np.interp(new_thresholds, thresholds, tpr)
        thresholds = new_thresholds
        fpr = new_fpr
        tpr = new_tpr

    return ROCCurve(
        false_positive_rates=cast(list[float], fpr.tolist()),
        true_positive_rates=cast(list[float], tpr.tolist()),
        thresholds=cast(list[float], thresholds.tolist()),
    )


@dataclass
class ClassificationMetrics:
    coverage: float
    """Percentage of predictions that are not none"""

    f1_score: float
    """F1 score of the predictions"""

    accuracy: float
    """Accuracy of the predictions"""

    loss: float | None
    """Cross-entropy loss of the logits"""

    anomaly_score_mean: float | None = None
    """Mean of anomaly scores across the dataset"""

    anomaly_score_median: float | None = None
    """Median of anomaly scores across the dataset"""

    anomaly_score_variance: float | None = None
    """Variance of anomaly scores across the dataset"""

    roc_auc: float | None = None
    """Receiver operating characteristic area under the curve"""

    pr_auc: float | None = None
    """Average precision (area under the curve of the precision-recall curve)"""

    pr_curve: PRCurve | None = None
    """Precision-recall curve"""

    roc_curve: ROCCurve | None = None
    """Receiver operating characteristic curve"""

    def __repr__(self) -> str:
        return (
            "ClassificationMetrics({\n"
            + f"    accuracy: {self.accuracy:.4f},\n"
            + f"    f1_score: {self.f1_score:.4f},\n"
            + (f"    roc_auc: {self.roc_auc:.4f},\n" if self.roc_auc else "")
            + (f"    pr_auc: {self.pr_auc:.4f},\n" if self.pr_auc else "")
            + (
                f"    anomaly_score: {self.anomaly_score_mean:.4f} ± {self.anomaly_score_variance:.4f},\n"
                if self.anomaly_score_mean
                else ""
            )
            + "})"
        )


def convert_logits_to_probabilities(logits: NDArray[np.float32]) -> NDArray[np.float32]:
    """
    Convert logits to probability distributions.

    This function handles multiple input formats:
    - 1D arrays: Binary classification probabilities (must be between 0 and 1)
    - 2D arrays: Multi-class logits or probabilities

    For 2D inputs, the function automatically detects the format:
    - If any values are <= 0: applies softmax (raw logits)
    - If rows don't sum to 1: normalizes to probabilities
    - If rows sum to 1: treats as already normalized probabilities

    Args:
        logits: Input logits or probabilities as a float32 numpy array.
            Can be 1D (binary) or 2D (multi-class). May contain NaN values.

    Returns:
        A 2D float32 numpy array of probabilities with shape (n_samples, n_classes).
        Each row sums to 1.0 (except for rows with all NaN values).

    Raises:
        ValueError: If logits are not 1D or 2D
        ValueError: If 1D logits are not between 0 and 1 (for binary classification)
        ValueError: If 2D logits have fewer than 2 classes (use regression metrics instead)
    """
    if logits.ndim == 1:
        # Binary classification: 1D probabilities
        # Check non-NaN values only
        valid_logits = logits[~np.isnan(logits)]
        if len(valid_logits) > 0 and ((valid_logits > 1).any() or (valid_logits < 0).any()):
            raise ValueError("Logits must be between 0 and 1 for binary classification")
        # Convert 1D probabilities to 2D format: [1-p, p]
        probabilities = cast(NDArray[np.float32], np.column_stack([1 - logits, logits]))
    elif logits.ndim == 2:
        if logits.shape[1] < 2:
            raise ValueError("Use a different metric function for regression tasks")
        # Check if any non-NaN values are <= 0 (NaN-aware comparison)
        valid_logits = logits[~np.isnan(logits)]
        if len(valid_logits) > 0 and not (valid_logits > 0).all():
            # Contains negative values or zeros: apply softmax (raw logits)
            probabilities = cast(NDArray[np.float32], softmax(logits))
        elif not np.allclose(logits.sum(-1, keepdims=True), 1.0):
            # Rows don't sum to 1: normalize to probabilities
            probabilities = cast(NDArray[np.float32], logits / logits.sum(-1, keepdims=True))
        else:
            # Already normalized probabilities
            probabilities = logits
    else:
        raise ValueError("Logits must be 1 or 2 dimensional")

    return probabilities


def calculate_classification_metrics(
    expected_labels: list[int] | NDArray[np.int64],
    logits: list[list[float]] | list[NDArray[np.float32]] | NDArray[np.float32],
    anomaly_scores: list[float] | None = None,
    average: Literal["micro", "macro", "weighted", "binary"] | None = None,
    multi_class: Literal["ovr", "ovo"] = "ovr",
    include_curves: bool = False,
) -> ClassificationMetrics:
    references = np.array(expected_labels)

    # Convert to numpy array, handling None values
    logits = convert_to_float32_array(logits)

    # Check if all logits are NaN (all predictions are None/NaN)
    if np.all(np.isnan(logits)):
        # Return placeholder metrics when all logits are invalid
        return ClassificationMetrics(
            coverage=0.0,
            f1_score=0.0,
            accuracy=0.0,
            loss=None,
            anomaly_score_mean=None,
            anomaly_score_median=None,
            anomaly_score_variance=None,
            roc_auc=None,
            pr_auc=None,
            pr_curve=None,
            roc_curve=None,
        )

    # Convert logits to probabilities
    probabilities = convert_logits_to_probabilities(logits)

    predictions = np.argmax(probabilities, axis=-1)
    predictions[np.isnan(probabilities).all(axis=-1)] = -1  # set predictions to -1 for all nan logits

    num_classes_references = len(set(references))
    num_classes_predictions = len(set(predictions))
    num_none_predictions = np.isnan(probabilities).all(axis=-1).sum()
    coverage = 1 - num_none_predictions / len(probabilities)

    if average is None:
        average = "binary" if num_classes_references == 2 and num_none_predictions == 0 else "weighted"

    accuracy = sklearn.metrics.accuracy_score(references, predictions)
    f1 = sklearn.metrics.f1_score(references, predictions, average=average)
    # Ensure sklearn sees the full class set corresponding to probability columns
    # to avoid errors when y_true does not contain all classes.
    loss = (
        sklearn.metrics.log_loss(
            references,
            probabilities,
            labels=list(range(probabilities.shape[1])),
        )
        if num_none_predictions == 0
        else None
    )

    if num_classes_references == num_classes_predictions and num_none_predictions == 0:
        # special case for binary classification: https://github.com/scikit-learn/scikit-learn/issues/20186
        if num_classes_references == 2:
            # Use probabilities[:, 1] which is guaranteed to be 2D
            probabilities_positive = probabilities[:, 1]
            roc_auc = sklearn.metrics.roc_auc_score(references, probabilities_positive)
            roc_curve = calculate_roc_curve(references, probabilities_positive) if include_curves else None
            pr_auc = sklearn.metrics.average_precision_score(references, probabilities_positive)
            pr_curve = calculate_pr_curve(references, probabilities_positive) if include_curves else None
        else:
            roc_auc = sklearn.metrics.roc_auc_score(references, probabilities, multi_class=multi_class)
            roc_curve = None
            pr_auc = None
            pr_curve = None
    else:
        roc_auc = None
        pr_auc = None
        pr_curve = None
        roc_curve = None

    # Calculate anomaly score statistics
    anomaly_score_mean, anomaly_score_median, anomaly_score_variance = calculate_anomaly_score_stats(anomaly_scores)

    return ClassificationMetrics(
        coverage=coverage,
        accuracy=float(accuracy),
        f1_score=float(f1),
        loss=float(loss) if loss is not None else None,
        anomaly_score_mean=anomaly_score_mean,
        anomaly_score_median=anomaly_score_median,
        anomaly_score_variance=anomaly_score_variance,
        roc_auc=float(roc_auc) if roc_auc is not None else None,
        pr_auc=float(pr_auc) if pr_auc is not None else None,
        pr_curve=pr_curve,
        roc_curve=roc_curve,
    )


@dataclass
class RegressionMetrics:
    coverage: float
    """Percentage of predictions that are not none"""

    mse: float
    """Mean squared error of the predictions"""

    rmse: float
    """Root mean squared error of the predictions"""

    mae: float
    """Mean absolute error of the predictions"""

    r2: float
    """R-squared score (coefficient of determination) of the predictions"""

    explained_variance: float
    """Explained variance score of the predictions"""

    loss: float
    """Mean squared error loss of the predictions"""

    anomaly_score_mean: float | None = None
    """Mean of anomaly scores across the dataset"""

    anomaly_score_median: float | None = None
    """Median of anomaly scores across the dataset"""

    anomaly_score_variance: float | None = None
    """Variance of anomaly scores across the dataset"""

    def __repr__(self) -> str:
        return (
            "RegressionMetrics({\n"
            + f"    mae: {self.mae:.4f},\n"
            + f"    rmse: {self.rmse:.4f},\n"
            + f"    r2: {self.r2:.4f},\n"
            + (
                f"    anomaly_score: {self.anomaly_score_mean:.4f} ± {self.anomaly_score_variance:.4f},\n"
                if self.anomaly_score_mean
                else ""
            )
            + "})"
        )


def calculate_regression_metrics(
    expected_scores: NDArray[np.float32] | Sequence[float],
    predicted_scores: NDArray[np.float32] | Sequence[float | None],
    anomaly_scores: NDArray[np.float32] | Sequence[float] | None = None,
) -> RegressionMetrics:
    """
    Calculate regression metrics for model evaluation.

    Params:
        references: True target values
        predictions: Predicted values from the model
        anomaly_scores: Optional anomaly scores for each prediction

    Returns:
        Comprehensive regression metrics including MSE, RMSE, MAE, R², and explained variance

    Raises:
        ValueError: If predictions and references have different lengths
        ValueError: If expected_scores contains None or NaN values
    """
    # Convert to numpy arrays, handling None values
    references = convert_to_float32_array(expected_scores)
    predictions = convert_to_float32_array(predicted_scores)

    if len(predictions) != len(references):
        raise ValueError("Predictions and references must have the same length")

    # Validate that all expected_scores are non-None and non-NaN
    if np.any(np.isnan(references)):
        raise ValueError("expected_scores must not contain None or NaN values")

    # If all of the predictions are None or NaN, return None for all metrics
    if np.all(np.isnan(predictions)):
        anomaly_score_mean, anomaly_score_median, anomaly_score_variance = calculate_anomaly_score_stats(anomaly_scores)
        return RegressionMetrics(
            coverage=0.0,
            mse=0.0,
            rmse=0.0,
            mae=0.0,
            r2=0.0,
            explained_variance=0.0,
            loss=0.0,
            anomaly_score_mean=anomaly_score_mean,
            anomaly_score_median=anomaly_score_median,
            anomaly_score_variance=anomaly_score_variance,
        )

    # Filter out NaN values from predictions (expected_scores are already validated to be non-NaN)
    valid_mask = ~np.isnan(predictions)
    num_none_predictions = (~valid_mask).sum()
    coverage = 1 - num_none_predictions / len(predictions)
    if num_none_predictions > 0:
        references = references[valid_mask]
        predictions = predictions[valid_mask]

    # Calculate core regression metrics
    mse = float(sklearn.metrics.mean_squared_error(references, predictions))
    rmse = float(np.sqrt(mse))
    mae = float(sklearn.metrics.mean_absolute_error(references, predictions))
    r2 = float(sklearn.metrics.r2_score(references, predictions))
    explained_var = float(sklearn.metrics.explained_variance_score(references, predictions))

    # Calculate anomaly score statistics
    anomaly_score_mean, anomaly_score_median, anomaly_score_variance = calculate_anomaly_score_stats(anomaly_scores)

    return RegressionMetrics(
        coverage=coverage,
        mse=mse,
        rmse=rmse,
        mae=mae,
        r2=r2,
        explained_variance=explained_var,
        loss=mse,  # For regression, loss is typically MSE
        anomaly_score_mean=anomaly_score_mean,
        anomaly_score_median=anomaly_score_median,
        anomaly_score_variance=anomaly_score_variance,
    )
