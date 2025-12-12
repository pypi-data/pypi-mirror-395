from uuid import uuid4

import numpy as np
import pytest
from datasets.arrow_dataset import Dataset

from .datasource import Datasource
from .embedding_model import PretrainedEmbeddingModel
from .memoryset import ScoredMemoryset
from .regression_model import RegressionMetrics, RegressionModel
from .telemetry import RegressionPrediction


def test_create_model(regression_model: RegressionModel, scored_memoryset: ScoredMemoryset):
    assert regression_model is not None
    assert regression_model.name == "test_regression_model"
    assert regression_model.memoryset == scored_memoryset
    assert regression_model.memory_lookup_count == 3


def test_create_model_already_exists_error(scored_memoryset, regression_model: RegressionModel):
    with pytest.raises(ValueError):
        RegressionModel.create("test_regression_model", scored_memoryset)
    with pytest.raises(ValueError):
        RegressionModel.create("test_regression_model", scored_memoryset, if_exists="error")


def test_create_model_already_exists_return(scored_memoryset, regression_model: RegressionModel):
    with pytest.raises(ValueError):
        RegressionModel.create("test_regression_model", scored_memoryset, if_exists="open", memory_lookup_count=37)

    new_model = RegressionModel.create("test_regression_model", scored_memoryset, if_exists="open")
    assert new_model is not None
    assert new_model.name == "test_regression_model"
    assert new_model.memoryset == scored_memoryset
    assert new_model.memory_lookup_count == 3


def test_create_model_unauthenticated(unauthenticated_client, scored_memoryset: ScoredMemoryset):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            RegressionModel.create("test_regression_model", scored_memoryset)


def test_get_model(regression_model: RegressionModel):
    fetched_model = RegressionModel.open(regression_model.name)
    assert fetched_model is not None
    assert fetched_model.id == regression_model.id
    assert fetched_model.name == regression_model.name
    assert fetched_model.memory_lookup_count == 3
    assert fetched_model == regression_model


def test_get_model_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            RegressionModel.open("test_regression_model")


def test_get_model_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        RegressionModel.open("not valid id")


def test_get_model_not_found():
    with pytest.raises(LookupError):
        RegressionModel.open(str(uuid4()))


def test_get_model_unauthorized(unauthorized_client, regression_model: RegressionModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            RegressionModel.open(regression_model.name)


def test_list_models(regression_model: RegressionModel):
    models = RegressionModel.all()
    assert len(models) > 0
    assert any(model.name == regression_model.name for model in models)


def test_list_models_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            RegressionModel.all()


def test_list_models_unauthorized(unauthorized_client, regression_model: RegressionModel):
    with unauthorized_client.use():
        assert RegressionModel.all() == []


def test_update_model_attributes(regression_model: RegressionModel):
    regression_model.description = "New description"
    assert regression_model.description == "New description"

    regression_model.set(description=None)
    assert regression_model.description is None

    regression_model.set(locked=True)
    assert regression_model.locked is True

    regression_model.set(locked=False)
    assert regression_model.locked is False

    regression_model.lock()
    assert regression_model.locked is True

    regression_model.unlock()
    assert regression_model.locked is False


def test_delete_model(scored_memoryset: ScoredMemoryset):
    RegressionModel.create("regression_model_to_delete", ScoredMemoryset.open(scored_memoryset.name))
    assert RegressionModel.open("regression_model_to_delete")
    RegressionModel.drop("regression_model_to_delete")
    with pytest.raises(LookupError):
        RegressionModel.open("regression_model_to_delete")


def test_delete_model_unauthenticated(unauthenticated_client, regression_model: RegressionModel):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            RegressionModel.drop(regression_model.name)


def test_delete_model_not_found():
    with pytest.raises(LookupError):
        RegressionModel.drop(str(uuid4()))
    # ignores error if specified
    RegressionModel.drop(str(uuid4()), if_not_exists="ignore")


def test_delete_model_unauthorized(unauthorized_client, regression_model: RegressionModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            RegressionModel.drop(regression_model.name)


def test_delete_memoryset_before_model_constraint_violation(hf_dataset):
    memoryset = ScoredMemoryset.from_hf_dataset("test_memoryset_delete_before_regression_model", hf_dataset)
    RegressionModel.create("test_regression_model_delete_before_memoryset", memoryset)
    with pytest.raises(RuntimeError):
        ScoredMemoryset.drop(memoryset.id)


@pytest.mark.parametrize("data_type", ["dataset", "datasource"])
def test_evaluate(
    regression_model: RegressionModel,
    eval_datasource: Datasource,
    eval_dataset: Dataset,
    data_type,
):
    """Test that model evaluation with a dataset works."""
    result = (
        regression_model.evaluate(eval_dataset)
        if data_type == "dataset"
        else regression_model.evaluate(eval_datasource)
    )

    assert isinstance(result, RegressionMetrics)
    assert np.allclose(result.mae, 0.4)
    assert 0.0 <= result.mse <= 1.0
    assert 0.0 <= result.rmse <= 1.0
    assert result.r2 is not None

    assert isinstance(result.anomaly_score_mean, float)
    assert isinstance(result.anomaly_score_median, float)
    assert isinstance(result.anomaly_score_variance, float)
    assert -1.0 <= result.anomaly_score_mean <= 1.0
    assert -1.0 <= result.anomaly_score_median <= 1.0
    assert -1.0 <= result.anomaly_score_variance <= 1.0


def test_evaluate_datasource_with_nones_raises_error(regression_model: RegressionModel, datasource: Datasource):
    with pytest.raises(ValueError):
        regression_model.evaluate(datasource, record_predictions=True, tags={"test"})


def test_evaluate_dataset_with_nones_raises_error(regression_model: RegressionModel, hf_dataset: Dataset):
    with pytest.raises(ValueError):
        regression_model.evaluate(hf_dataset, record_predictions=True, tags={"test"})


def test_evaluate_with_telemetry(regression_model, eval_dataset: Dataset):
    result = regression_model.evaluate(eval_dataset, record_predictions=True, tags={"test"})
    assert result is not None
    assert isinstance(result, RegressionMetrics)
    predictions = regression_model.predictions(tag="test")
    assert len(predictions) == 4
    assert all(p.tags == {"test"} for p in predictions)
    assert all(p.expected_score is not None for p in predictions)
    assert all(np.allclose(p.expected_score, s) for p, s in zip(predictions, eval_dataset["score"]))


def test_evaluate_with_partition_column_dataset(partitioned_regression_model: RegressionModel):
    """Test evaluate with partition_column on a Dataset"""
    # Create a test dataset with partition_id column
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "score": 0.1, "partition_id": "p1"},
            {"value": "cats are cute", "score": 0.9, "partition_id": "p1"},
            {"value": "homemade soup recipes", "score": 0.1, "partition_id": "p2"},
            {"value": "cats purr when happy", "score": 0.9, "partition_id": "p2"},
        ]
    )

    # Evaluate with partition_column
    result = partitioned_regression_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="exclude_global",
    )
    assert result is not None
    assert isinstance(result, RegressionMetrics)
    assert isinstance(result.mae, float)
    assert isinstance(result.mse, float)
    assert isinstance(result.rmse, float)
    assert result.r2 is not None


def test_evaluate_with_partition_column_include_global(partitioned_regression_model: RegressionModel):
    """Test evaluate with partition_column and include_global mode"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "score": 0.1, "partition_id": "p1"},
            {"value": "cats are cute", "score": 0.9, "partition_id": "p1"},
        ]
    )

    # Evaluate with partition_column and include_global (default)
    result = partitioned_regression_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="include_global",
    )
    assert result is not None
    assert isinstance(result, RegressionMetrics)


def test_evaluate_with_partition_column_exclude_global(partitioned_regression_model: RegressionModel):
    """Test evaluate with partition_column and exclude_global mode"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "score": 0.1, "partition_id": "p1"},
            {"value": "cats are cute", "score": 0.9, "partition_id": "p1"},
        ]
    )

    # Evaluate with partition_column and exclude_global
    result = partitioned_regression_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="exclude_global",
    )
    assert result is not None
    assert isinstance(result, RegressionMetrics)


def test_evaluate_with_partition_column_only_global(partitioned_regression_model: RegressionModel):
    """Test evaluate with partition_filter_mode only_global"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "cats are independent animals", "score": 0.9, "partition_id": None},
            {"value": "i love the beach", "score": 0.5, "partition_id": None},
        ]
    )

    # Evaluate with only_global mode
    result = partitioned_regression_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="only_global",
    )
    assert result is not None
    assert isinstance(result, RegressionMetrics)


def test_evaluate_with_partition_column_ignore_partitions(partitioned_regression_model: RegressionModel):
    """Test evaluate with partition_filter_mode ignore_partitions"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "score": 0.1, "partition_id": "p1"},
            {"value": "cats are cute", "score": 0.9, "partition_id": "p2"},
        ]
    )

    # Evaluate with ignore_partitions mode
    result = partitioned_regression_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="ignore_partitions",
    )
    assert result is not None
    assert isinstance(result, RegressionMetrics)


@pytest.mark.parametrize("data_type", ["dataset", "datasource"])
def test_evaluate_with_partition_column_datasource(partitioned_regression_model: RegressionModel, data_type):
    """Test evaluate with partition_column on a Datasource"""
    # Create a test datasource with partition_id column
    eval_data_with_partition = [
        {"value": "soup is good", "score": 0.1, "partition_id": "p1"},
        {"value": "cats are cute", "score": 0.9, "partition_id": "p1"},
        {"value": "homemade soup recipes", "score": 0.1, "partition_id": "p2"},
        {"value": "cats purr when happy", "score": 0.9, "partition_id": "p2"},
    ]

    if data_type == "dataset":
        eval_data = Dataset.from_list(eval_data_with_partition)
        result = partitioned_regression_model.evaluate(
            eval_data,
            partition_column="partition_id",
            partition_filter_mode="exclude_global",
        )
    else:
        eval_datasource = Datasource.from_list("eval_datasource_with_partition_regression", eval_data_with_partition)
        result = partitioned_regression_model.evaluate(
            eval_datasource,
            partition_column="partition_id",
            partition_filter_mode="exclude_global",
        )

    assert result is not None
    assert isinstance(result, RegressionMetrics)
    assert isinstance(result.mae, float)
    assert isinstance(result.mse, float)


def test_predict(regression_model: RegressionModel):
    predictions = regression_model.predict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2
    assert predictions[0].prediction_id is not None
    assert predictions[1].prediction_id is not None
    assert np.allclose(predictions[0].score, 0.1)
    assert np.allclose(predictions[1].score, 0.9)
    assert 0 <= predictions[0].confidence <= 1
    assert 0 <= predictions[1].confidence <= 1


def test_regression_prediction_has_no_score(regression_model: RegressionModel):
    """Ensure optional score is None for regression predictions."""
    prediction = regression_model.predict("This beach is amazing!")
    assert isinstance(prediction, RegressionPrediction)
    assert prediction.score is None


def test_predict_unauthenticated(unauthenticated_client, regression_model: RegressionModel):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            regression_model.predict(["This is excellent!", "This is terrible!"])


def test_predict_unauthorized(unauthorized_client, regression_model: RegressionModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            regression_model.predict(["This is excellent!", "This is terrible!"])


def test_predict_constraint_violation(scored_memoryset: ScoredMemoryset):
    model = RegressionModel.create(
        "test_regression_model_lookup_count_too_high",
        scored_memoryset,
        memory_lookup_count=scored_memoryset.length + 2,
    )
    with pytest.raises(RuntimeError):
        model.predict("test")


def test_predict_with_prompt(regression_model: RegressionModel):
    """Test that prompt parameter is properly passed through to predictions"""
    # Test with an instruction-supporting embedding model if available
    prediction_with_prompt = regression_model.predict(
        "This product is amazing!", prompt="Represent this text for rating prediction:"
    )
    prediction_without_prompt = regression_model.predict("This product is amazing!")

    # Both should work and return valid predictions
    assert prediction_with_prompt.score is not None
    assert prediction_without_prompt.score is not None
    assert 0 <= prediction_with_prompt.confidence <= 1
    assert 0 <= prediction_without_prompt.confidence <= 1


def test_predict_with_partition_id(partitioned_regression_model: RegressionModel):
    """Test predict with a specific partition_id"""
    # Predict with partition_id p1 - should use memories from p1
    prediction = partitioned_regression_model.predict("soup", partition_id="p1", partition_filter_mode="exclude_global")
    assert prediction.score is not None
    assert 0 <= prediction.confidence <= 1

    # Predict with partition_id p2 - should use memories from p2
    prediction_p2 = partitioned_regression_model.predict(
        "cats", partition_id="p2", partition_filter_mode="exclude_global"
    )
    assert prediction_p2.score is not None
    assert 0 <= prediction_p2.confidence <= 1


def test_predict_with_partition_id_include_global(partitioned_regression_model: RegressionModel):
    """Test predict with partition_id and include_global mode (default)"""
    # Predict with partition_id p1 and include_global (default) - should include both p1 and global memories
    prediction = partitioned_regression_model.predict("soup", partition_id="p1", partition_filter_mode="include_global")
    assert prediction.score is not None
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_exclude_global(partitioned_regression_model: RegressionModel):
    """Test predict with partition_id and exclude_global mode"""
    # Predict with partition_id p1 and exclude_global - should only use p1 memories
    prediction = partitioned_regression_model.predict("soup", partition_id="p1", partition_filter_mode="exclude_global")
    assert prediction.score is not None
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_only_global(partitioned_regression_model: RegressionModel):
    """Test predict with partition_filter_mode only_global"""
    # Predict with only_global mode - should only use global memories
    prediction = partitioned_regression_model.predict("cats", partition_filter_mode="only_global")
    assert prediction.score is not None
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_ignore_partitions(partitioned_regression_model: RegressionModel):
    """Test predict with partition_filter_mode ignore_partitions"""
    # Predict with ignore_partitions mode - should ignore partition filtering
    prediction = partitioned_regression_model.predict("soup", partition_filter_mode="ignore_partitions")
    assert prediction.score is not None
    assert 0 <= prediction.confidence <= 1


def test_predict_batch_with_partition_id(partitioned_regression_model: RegressionModel):
    """Test batch predict with partition_id"""
    # Batch predict with partition_id p1
    predictions = partitioned_regression_model.predict(
        ["soup is good", "cats are cute"],
        partition_id="p1",
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.score is not None for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)


def test_predict_batch_with_list_of_partition_ids(partitioned_regression_model: RegressionModel):
    """Test batch predict with a list of partition_ids (one for each query input)"""
    # Batch predict with a list of partition_ids - one for each input
    # First input uses p1, second input uses p2
    predictions = partitioned_regression_model.predict(
        ["soup is good", "cats are cute"],
        partition_id=["p1", "p2"],
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.score is not None for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)

    # Verify that predictions were made using the correct partitions
    # Each prediction should use memories from its respective partition
    assert predictions[0].input_value == "soup is good"
    assert predictions[1].input_value == "cats are cute"


def test_record_prediction_feedback(regression_model: RegressionModel):
    predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
    expected_scores = [0.9, 0.1]
    regression_model.record_feedback(
        {
            "prediction_id": p.prediction_id,
            "category": "accurate",
            "value": abs(p.score - expected_score) < 0.2,
        }
        for expected_score, p in zip(expected_scores, predictions)
    )


def test_record_prediction_feedback_missing_category(regression_model: RegressionModel):
    prediction = regression_model.predict("This is excellent!")
    with pytest.raises(ValueError):
        regression_model.record_feedback({"prediction_id": prediction.prediction_id, "value": True})


def test_record_prediction_feedback_invalid_value(regression_model: RegressionModel):
    prediction = regression_model.predict("This is excellent!")
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        regression_model.record_feedback(
            {"prediction_id": prediction.prediction_id, "category": "accurate", "value": "invalid"}
        )


def test_record_prediction_feedback_invalid_prediction_id(regression_model: RegressionModel):
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        regression_model.record_feedback({"prediction_id": "invalid", "category": "accurate", "value": True})


def test_predict_with_memoryset_override(regression_model: RegressionModel, hf_dataset: Dataset):
    # Create a memoryset with different scores
    inverted_scored_memoryset = ScoredMemoryset.from_hf_dataset(
        "test_memoryset_inverted_scores",
        hf_dataset.map(lambda x: {"score": (2.0 - x["score"]) if x["score"] is not None else None}),  # Invert scores
        embedding_model=PretrainedEmbeddingModel.GTE_BASE,
    )
    original_predictions = regression_model.predict(["This is excellent!", "This is terrible!"])

    with regression_model.use_memoryset(inverted_scored_memoryset):
        override_predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
        # With inverted scores, the predictions should be different
        assert abs(override_predictions[0].score - original_predictions[0].score) > 0.1
        assert abs(override_predictions[1].score - original_predictions[1].score) > 0.1

    # After exiting context, predictions should be back to normal
    new_predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
    assert abs(new_predictions[0].score - original_predictions[0].score) < 0.1
    assert abs(new_predictions[1].score - original_predictions[1].score) < 0.1


def test_predict_with_expected_scores(regression_model: RegressionModel):
    prediction = regression_model.predict("This is excellent!", expected_scores=0.9)
    assert prediction.expected_score == 0.9


def test_regression_prediction_update(regression_model: RegressionModel):
    prediction = regression_model.predict("Test input", expected_scores=3.5)
    assert prediction.expected_score == 3.5
    assert prediction.tags == set()

    # Update expected score
    prediction.update(expected_score=4.5)
    assert prediction.expected_score == 4.5

    # Add tags
    prediction.update(tags={"test", "updated"})
    assert prediction.tags == {"test", "updated"}

    # Clear both
    prediction.update(expected_score=None, tags=None)
    assert prediction.expected_score is None
    assert prediction.tags == set()


def test_last_prediction_with_batch(regression_model: RegressionModel):
    predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
    assert regression_model.last_prediction is not None
    assert regression_model.last_prediction.prediction_id == predictions[-1].prediction_id
    assert regression_model.last_prediction.input_value == "This is terrible!"
    assert regression_model._last_prediction_was_batch is True


def test_last_prediction_with_single(regression_model: RegressionModel):
    # Test that last_prediction is updated correctly with single prediction
    prediction = regression_model.predict("This is excellent!")
    assert regression_model.last_prediction is not None
    assert regression_model.last_prediction.prediction_id == prediction.prediction_id
    assert regression_model.last_prediction.input_value == "This is excellent!"
    assert regression_model._last_prediction_was_batch is False


def test_batch_predict(regression_model: RegressionModel):
    """Test batch predictions"""
    predictions = regression_model.predict(["test input 1", "test input 2", "test input 3"])
    assert len(predictions) == 3
    assert all(isinstance(pred, RegressionPrediction) for pred in predictions)


def test_batch_predict_with_expected_scores(regression_model: RegressionModel):
    """Test batch predictions with expected scores"""
    predictions = regression_model.predict(["input 1", "input 2"], expected_scores=[0.5, 0.8])
    assert len(predictions) == 2
    assert all(isinstance(pred, RegressionPrediction) for pred in predictions)


def test_use_memoryset(regression_model: RegressionModel, scored_memoryset: ScoredMemoryset):
    # Test that predictions work with a memoryset
    predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
    assert len(predictions) == 2
    assert all(isinstance(pred, RegressionPrediction) for pred in predictions)
    assert all(0 <= pred.confidence <= 1 for pred in predictions)

    # Test that predictions work with a different memoryset
    with regression_model.use_memoryset(scored_memoryset):
        predictions = regression_model.predict(["This is excellent!", "This is terrible!"])
        assert len(predictions) == 2
        assert all(isinstance(pred, RegressionPrediction) for pred in predictions)
        assert all(0 <= pred.confidence <= 1 for pred in predictions)


def test_drop(regression_model):
    """Test that model drop works."""
    name = regression_model.name
    RegressionModel.drop(name)
    assert not RegressionModel.exists(name)
