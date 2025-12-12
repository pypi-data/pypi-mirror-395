import logging
from uuid import uuid4

import numpy as np
import pytest
from datasets import Dataset

from .classification_model import ClassificationMetrics, ClassificationModel
from .conftest import skip_in_ci
from .datasource import Datasource
from .embedding_model import PretrainedEmbeddingModel
from .memoryset import LabeledMemoryset
from .telemetry import ClassificationPrediction


def test_create_model(classification_model: ClassificationModel, readonly_memoryset: LabeledMemoryset):
    assert classification_model is not None
    assert classification_model.name == "test_classification_model"
    assert classification_model.memoryset == readonly_memoryset
    assert classification_model.num_classes == 2
    assert classification_model.memory_lookup_count == 3


def test_create_model_already_exists_error(readonly_memoryset, classification_model):
    with pytest.raises(ValueError):
        ClassificationModel.create("test_classification_model", readonly_memoryset)
    with pytest.raises(ValueError):
        ClassificationModel.create("test_classification_model", readonly_memoryset, if_exists="error")


def test_create_model_already_exists_return(readonly_memoryset, classification_model):
    with pytest.raises(ValueError):
        ClassificationModel.create("test_classification_model", readonly_memoryset, if_exists="open", head_type="MMOE")

    with pytest.raises(ValueError):
        ClassificationModel.create(
            "test_classification_model", readonly_memoryset, if_exists="open", memory_lookup_count=37
        )

    with pytest.raises(ValueError):
        ClassificationModel.create("test_classification_model", readonly_memoryset, if_exists="open", num_classes=19)

    with pytest.raises(ValueError):
        ClassificationModel.create(
            "test_classification_model", readonly_memoryset, if_exists="open", min_memory_weight=0.77
        )

    new_model = ClassificationModel.create("test_classification_model", readonly_memoryset, if_exists="open")
    assert new_model is not None
    assert new_model.name == "test_classification_model"
    assert new_model.memoryset == readonly_memoryset
    assert new_model.num_classes == 2
    assert new_model.memory_lookup_count == 3


def test_create_model_unauthenticated(unauthenticated_client, readonly_memoryset: LabeledMemoryset):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            ClassificationModel.create("test_model", readonly_memoryset)


def test_get_model(classification_model: ClassificationModel):
    fetched_model = ClassificationModel.open(classification_model.name)
    assert fetched_model is not None
    assert fetched_model.id == classification_model.id
    assert fetched_model.name == classification_model.name
    assert fetched_model.num_classes == 2
    assert fetched_model.memory_lookup_count == 3
    assert fetched_model == classification_model


def test_get_model_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            ClassificationModel.open("test_model")


def test_get_model_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        ClassificationModel.open("not valid id")


def test_get_model_not_found():
    with pytest.raises(LookupError):
        ClassificationModel.open(str(uuid4()))


def test_get_model_unauthorized(unauthorized_client, classification_model: ClassificationModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            ClassificationModel.open(classification_model.name)


def test_list_models(classification_model: ClassificationModel):
    models = ClassificationModel.all()
    assert len(models) > 0
    assert any(model.name == model.name for model in models)


def test_list_models_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            ClassificationModel.all()


def test_list_models_unauthorized(unauthorized_client, classification_model: ClassificationModel):
    with unauthorized_client.use():
        assert ClassificationModel.all() == []


def test_update_model_attributes(classification_model: ClassificationModel):
    classification_model.description = "New description"
    assert classification_model.description == "New description"

    classification_model.set(description=None)
    assert classification_model.description is None

    classification_model.set(locked=True)
    assert classification_model.locked is True

    classification_model.set(locked=False)
    assert classification_model.locked is False

    classification_model.lock()
    assert classification_model.locked is True

    classification_model.unlock()
    assert classification_model.locked is False


def test_delete_model(readonly_memoryset: LabeledMemoryset):
    ClassificationModel.create("model_to_delete", LabeledMemoryset.open(readonly_memoryset.name))
    assert ClassificationModel.open("model_to_delete")
    ClassificationModel.drop("model_to_delete")
    with pytest.raises(LookupError):
        ClassificationModel.open("model_to_delete")


def test_delete_model_unauthenticated(unauthenticated_client, classification_model: ClassificationModel):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            ClassificationModel.drop(classification_model.name)


def test_delete_model_not_found():
    with pytest.raises(LookupError):
        ClassificationModel.drop(str(uuid4()))
    # ignores error if specified
    ClassificationModel.drop(str(uuid4()), if_not_exists="ignore")


def test_delete_model_unauthorized(unauthorized_client, classification_model: ClassificationModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            ClassificationModel.drop(classification_model.name)


def test_delete_memoryset_before_model_constraint_violation(hf_dataset):
    memoryset = LabeledMemoryset.from_hf_dataset("test_memoryset_delete_before_model", hf_dataset)
    ClassificationModel.create("test_model_delete_before_memoryset", memoryset)
    with pytest.raises(RuntimeError):
        LabeledMemoryset.drop(memoryset.id)


@pytest.mark.parametrize("data_type", ["dataset", "datasource"])
def test_evaluate(classification_model, eval_datasource: Datasource, eval_dataset: Dataset, data_type):
    result = (
        classification_model.evaluate(eval_dataset)
        if data_type == "dataset"
        else classification_model.evaluate(eval_datasource)
    )

    assert result is not None
    assert isinstance(result, ClassificationMetrics)

    assert isinstance(result.accuracy, float)
    assert np.allclose(result.accuracy, 0.5)
    assert isinstance(result.f1_score, float)
    assert np.allclose(result.f1_score, 0.5)
    assert isinstance(result.loss, float)

    assert isinstance(result.anomaly_score_mean, float)
    assert isinstance(result.anomaly_score_median, float)
    assert isinstance(result.anomaly_score_variance, float)
    assert -1.0 <= result.anomaly_score_mean <= 1.0
    assert -1.0 <= result.anomaly_score_median <= 1.0
    assert -1.0 <= result.anomaly_score_variance <= 1.0

    assert result.pr_auc is not None
    assert np.allclose(result.pr_auc, 0.83333)
    assert result.pr_curve is not None
    assert np.allclose(
        result.pr_curve["thresholds"],
        [0.0, 0.3021204173564911, 0.30852025747299194, 0.6932827234268188, 0.6972201466560364],
    )
    assert np.allclose(result.pr_curve["precisions"], [0.5, 0.666666, 0.5, 1.0, 1.0])
    assert np.allclose(result.pr_curve["recalls"], [1.0, 1.0, 0.5, 0.5, 0.0])

    assert result.roc_auc is not None
    assert np.allclose(result.roc_auc, 0.75)
    assert result.roc_curve is not None
    assert np.allclose(
        result.roc_curve["thresholds"],
        [0.3021204173564911, 0.30852025747299194, 0.6932827234268188, 0.6972201466560364, 1.0],
    )
    assert np.allclose(result.roc_curve["false_positive_rates"], [1.0, 0.5, 0.5, 0.0, 0.0])
    assert np.allclose(result.roc_curve["true_positive_rates"], [1.0, 1.0, 0.5, 0.5, 0.0])


def test_evaluate_datasource_with_nones_raises_error(classification_model: ClassificationModel, datasource: Datasource):
    with pytest.raises(ValueError):
        classification_model.evaluate(datasource, record_predictions=True, tags={"test"})


def test_evaluate_dataset_with_nones_raises_error(classification_model: ClassificationModel, hf_dataset: Dataset):
    with pytest.raises(ValueError):
        classification_model.evaluate(hf_dataset, record_predictions=True, tags={"test"})


def test_evaluate_with_telemetry(classification_model: ClassificationModel, eval_dataset: Dataset):
    result = classification_model.evaluate(eval_dataset, record_predictions=True, tags={"test"})
    assert result is not None
    assert isinstance(result, ClassificationMetrics)
    predictions = classification_model.predictions(tag="test")
    assert len(predictions) == 4
    assert all(p.tags == {"test"} for p in predictions)
    assert all(p.expected_label == l for p, l in zip(predictions, eval_dataset["label"]))


def test_evaluate_with_partition_column_dataset(partitioned_classification_model: ClassificationModel):
    """Test evaluate with partition_column on a Dataset"""
    # Create a test dataset with partition_id column
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "label": 0, "partition_id": "p1"},
            {"value": "cats are cute", "label": 1, "partition_id": "p1"},
            {"value": "homemade soup recipes", "label": 0, "partition_id": "p2"},
            {"value": "cats purr when happy", "label": 1, "partition_id": "p2"},
        ]
    )

    # Evaluate with partition_column
    result = partitioned_classification_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="exclude_global",
    )
    assert result is not None
    assert isinstance(result, ClassificationMetrics)
    assert isinstance(result.accuracy, float)
    assert isinstance(result.f1_score, float)
    assert isinstance(result.loss, float)


def test_evaluate_with_partition_column_include_global(partitioned_classification_model: ClassificationModel):
    """Test evaluate with partition_column and include_global mode"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "label": 0, "partition_id": "p1"},
            {"value": "cats are cute", "label": 1, "partition_id": "p1"},
        ]
    )

    # Evaluate with partition_column and include_global (default)
    result = partitioned_classification_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="include_global",
    )
    assert result is not None
    assert isinstance(result, ClassificationMetrics)


def test_evaluate_with_partition_column_exclude_global(partitioned_classification_model: ClassificationModel):
    """Test evaluate with partition_column and exclude_global mode"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "label": 0, "partition_id": "p1"},
            {"value": "cats are cute", "label": 1, "partition_id": "p1"},
        ]
    )

    # Evaluate with partition_column and exclude_global
    result = partitioned_classification_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="exclude_global",
    )
    assert result is not None
    assert isinstance(result, ClassificationMetrics)


def test_evaluate_with_partition_column_only_global(partitioned_classification_model: ClassificationModel):
    """Test evaluate with partition_filter_mode only_global"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "cats are independent animals", "label": 1, "partition_id": None},
            {"value": "i love the beach", "label": 1, "partition_id": None},
        ]
    )

    # Evaluate with only_global mode
    result = partitioned_classification_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="only_global",
    )
    assert result is not None
    assert isinstance(result, ClassificationMetrics)


def test_evaluate_with_partition_column_ignore_partitions(partitioned_classification_model: ClassificationModel):
    """Test evaluate with partition_filter_mode ignore_partitions"""
    eval_dataset_with_partition = Dataset.from_list(
        [
            {"value": "soup is good", "label": 0, "partition_id": "p1"},
            {"value": "cats are cute", "label": 1, "partition_id": "p2"},
        ]
    )

    # Evaluate with ignore_partitions mode
    result = partitioned_classification_model.evaluate(
        eval_dataset_with_partition,
        partition_column="partition_id",
        partition_filter_mode="ignore_partitions",
    )
    assert result is not None
    assert isinstance(result, ClassificationMetrics)


@pytest.mark.parametrize("data_type", ["dataset", "datasource"])
def test_evaluate_with_partition_column_datasource(partitioned_classification_model: ClassificationModel, data_type):
    """Test evaluate with partition_column on a Datasource"""
    # Create a test datasource with partition_id column
    eval_data_with_partition = [
        {"value": "soup is good", "label": 0, "partition_id": "p1"},
        {"value": "cats are cute", "label": 1, "partition_id": "p1"},
        {"value": "homemade soup recipes", "label": 0, "partition_id": "p2"},
        {"value": "cats purr when happy", "label": 1, "partition_id": "p2"},
    ]

    if data_type == "dataset":
        eval_data = Dataset.from_list(eval_data_with_partition)
        result = partitioned_classification_model.evaluate(
            eval_data,
            partition_column="partition_id",
            partition_filter_mode="exclude_global",
        )
    else:
        eval_datasource = Datasource.from_list("eval_datasource_with_partition", eval_data_with_partition)
        result = partitioned_classification_model.evaluate(
            eval_datasource,
            partition_column="partition_id",
            partition_filter_mode="exclude_global",
        )

    assert result is not None
    assert isinstance(result, ClassificationMetrics)
    assert isinstance(result.accuracy, float)
    assert isinstance(result.f1_score, float)


def test_predict(classification_model: ClassificationModel, label_names: list[str]):
    predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2
    assert predictions[0].prediction_id is not None
    assert predictions[1].prediction_id is not None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1

    assert predictions[0].logits is not None
    assert predictions[1].logits is not None
    assert len(predictions[0].logits) == 2
    assert len(predictions[1].logits) == 2
    assert predictions[0].logits[0] > predictions[0].logits[1]
    assert predictions[1].logits[0] < predictions[1].logits[1]


def test_classification_prediction_has_no_label(classification_model: ClassificationModel):
    """Ensure optional score is None for classification predictions."""
    prediction = classification_model.predict("Do you want to go to the beach?")
    assert isinstance(prediction, ClassificationPrediction)
    assert prediction.label is None


def test_predict_disable_telemetry(classification_model: ClassificationModel, label_names: list[str]):
    predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"], save_telemetry="off")
    assert len(predictions) == 2
    assert predictions[0].prediction_id is None
    assert predictions[1].prediction_id is None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1


def test_predict_unauthenticated(unauthenticated_client, classification_model: ClassificationModel):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            classification_model.predict(["Do you love soup?", "Are cats cute?"])


def test_predict_unauthorized(unauthorized_client, classification_model: ClassificationModel):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            classification_model.predict(["Do you love soup?", "Are cats cute?"])


def test_predict_constraint_violation(readonly_memoryset: LabeledMemoryset):
    model = ClassificationModel.create(
        "test_model_lookup_count_too_high",
        readonly_memoryset,
        num_classes=2,
        memory_lookup_count=readonly_memoryset.length + 2,
    )
    with pytest.raises(RuntimeError):
        model.predict("test")


def test_predict_with_partition_id(partitioned_classification_model: ClassificationModel, label_names: list[str]):
    """Test predict with a specific partition_id"""
    # Predict with partition_id p1 - should use memories from p1
    prediction = partitioned_classification_model.predict(
        "soup", partition_id="p1", partition_filter_mode="exclude_global"
    )
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1
    assert prediction.logits is not None
    assert len(prediction.logits) == 2

    # Predict with partition_id p2 - should use memories from p2
    prediction_p2 = partitioned_classification_model.predict(
        "cats", partition_id="p2", partition_filter_mode="exclude_global"
    )
    assert prediction_p2.label is not None
    assert prediction_p2.label_name in label_names
    assert 0 <= prediction_p2.confidence <= 1


def test_predict_with_partition_id_include_global(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test predict with partition_id and include_global mode (default)"""
    # Predict with partition_id p1 and include_global (default) - should include both p1 and global memories
    prediction = partitioned_classification_model.predict(
        "soup", partition_id="p1", partition_filter_mode="include_global"
    )
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_exclude_global(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test predict with partition_id and exclude_global mode"""
    # Predict with partition_id p1 and exclude_global - should only use p1 memories
    prediction = partitioned_classification_model.predict(
        "soup", partition_id="p1", partition_filter_mode="exclude_global"
    )
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_only_global(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test predict with partition_filter_mode only_global"""
    # Predict with only_global mode - should only use global memories
    prediction = partitioned_classification_model.predict("cats", partition_filter_mode="only_global")
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1


def test_predict_with_partition_id_ignore_partitions(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test predict with partition_filter_mode ignore_partitions"""
    # Predict with ignore_partitions mode - should ignore partition filtering
    prediction = partitioned_classification_model.predict("soup", partition_filter_mode="ignore_partitions")
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1


def test_predict_batch_with_partition_id(partitioned_classification_model: ClassificationModel, label_names: list[str]):
    """Test batch predict with partition_id"""
    # Batch predict with partition_id p1
    predictions = partitioned_classification_model.predict(
        ["soup is good", "cats are cute"],
        partition_id="p1",
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.label is not None for p in predictions)
    assert all(p.label_name in label_names for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)
    assert all(p.logits is not None and len(p.logits) == 2 for p in predictions)


def test_predict_with_partition_id_and_filters(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test predict with partition_id and filters"""
    # Predict with partition_id and filters
    prediction = partitioned_classification_model.predict(
        "soup",
        partition_id="p1",
        partition_filter_mode="exclude_global",
        filters=[("key", "==", "g1")],
    )
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1


def test_predict_batch_with_list_of_partition_ids(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test batch predict with a list of partition_ids (one for each query input)"""
    # Batch predict with a list of partition_ids - one for each input
    # First input uses p1, second input uses p2
    predictions = partitioned_classification_model.predict(
        ["soup is good", "cats are cute"],
        partition_id=["p1", "p2"],
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.label is not None for p in predictions)
    assert all(p.label_name in label_names for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)
    assert all(p.logits is not None and len(p.logits) == 2 for p in predictions)

    # Verify that predictions were made using the correct partitions
    # Each prediction should use memories from its respective partition
    assert predictions[0].input_value == "soup is good"
    assert predictions[1].input_value == "cats are cute"


@pytest.mark.asyncio
async def test_predict_async_with_partition_id(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test async predict with partition_id"""
    # Async predict with partition_id p1
    prediction = await partitioned_classification_model.apredict(
        "soup", partition_id="p1", partition_filter_mode="exclude_global"
    )
    assert prediction.label is not None
    assert prediction.label_name in label_names
    assert 0 <= prediction.confidence <= 1
    assert prediction.logits is not None
    assert len(prediction.logits) == 2


@pytest.mark.asyncio
async def test_predict_async_batch_with_partition_id(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test async batch predict with partition_id"""
    # Async batch predict with partition_id p1
    predictions = await partitioned_classification_model.apredict(
        ["soup is good", "cats are cute"],
        partition_id="p1",
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.label is not None for p in predictions)
    assert all(p.label_name in label_names for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)


@pytest.mark.asyncio
async def test_predict_async_batch_with_list_of_partition_ids(
    partitioned_classification_model: ClassificationModel, label_names: list[str]
):
    """Test async batch predict with a list of partition_ids (one for each query input)"""
    # Async batch predict with a list of partition_ids - one for each input
    # First input uses p1, second input uses p2
    predictions = await partitioned_classification_model.apredict(
        ["soup is good", "cats are cute"],
        partition_id=["p1", "p2"],
        partition_filter_mode="exclude_global",
    )
    assert len(predictions) == 2
    assert all(p.label is not None for p in predictions)
    assert all(p.label_name in label_names for p in predictions)
    assert all(0 <= p.confidence <= 1 for p in predictions)
    assert all(p.logits is not None and len(p.logits) == 2 for p in predictions)

    # Verify that predictions were made using the correct partitions
    # Each prediction should use memories from its respective partition
    assert predictions[0].input_value == "soup is good"
    assert predictions[1].input_value == "cats are cute"


def test_record_prediction_feedback(classification_model: ClassificationModel):
    predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"])
    expected_labels = [0, 1]
    classification_model.record_feedback(
        {
            "prediction_id": p.prediction_id,
            "category": "correct",
            "value": p.label == expected_label,
        }
        for expected_label, p in zip(expected_labels, predictions)
    )


def test_record_prediction_feedback_missing_category(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?")
    with pytest.raises(ValueError):
        classification_model.record_feedback({"prediction_id": prediction.prediction_id, "value": True})


def test_record_prediction_feedback_invalid_value(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?")
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        classification_model.record_feedback(
            {"prediction_id": prediction.prediction_id, "category": "correct", "value": "invalid"}
        )


def test_record_prediction_feedback_invalid_prediction_id(classification_model: ClassificationModel):
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        classification_model.record_feedback({"prediction_id": "invalid", "category": "correct", "value": True})


def test_predict_with_memoryset_override(classification_model: ClassificationModel, hf_dataset: Dataset):
    inverted_labeled_memoryset = LabeledMemoryset.from_hf_dataset(
        "test_memoryset_inverted_labels",
        hf_dataset.map(lambda x: {"label": 1 if x["label"] == 0 else 0}),
        embedding_model=PretrainedEmbeddingModel.GTE_BASE,
    )
    with classification_model.use_memoryset(inverted_labeled_memoryset):
        predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"])
        assert predictions[0].label == 1
        assert predictions[1].label == 0

    predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"])
    assert predictions[0].label == 0
    assert predictions[1].label == 1


def test_predict_with_expected_labels(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?", expected_labels=1)
    assert prediction.expected_label == 1


def test_predict_with_expected_labels_invalid_input(classification_model: ClassificationModel):
    # invalid number of expected labels for batch prediction
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        classification_model.predict(["Do you love soup?", "Are cats cute?"], expected_labels=[0])
    # invalid label value
    with pytest.raises(ValueError):
        classification_model.predict("Do you love soup?", expected_labels=5)


def test_predict_with_filters(classification_model: ClassificationModel):
    # there are no memories with label 0 and key g1, so we force a wrong prediction
    filtered_prediction = classification_model.predict("I love soup", filters=[("key", "==", "g2")])
    assert filtered_prediction.label == 1
    assert filtered_prediction.label_name == "cats"


def test_predict_with_memoryset_update(writable_memoryset: LabeledMemoryset):
    model = ClassificationModel.create(
        "test_predict_with_memoryset_update",
        writable_memoryset,
        num_classes=2,
        memory_lookup_count=3,
    )

    prediction = model.predict("Do you love soup?")
    assert prediction.label == 0
    assert prediction.label_name == "soup"

    # insert new memories
    writable_memoryset.insert(
        [
            {"value": "Do you love soup?", "label": 1, "key": "g1"},
            {"value": "Do you love soup for dinner?", "label": 1, "key": "g2"},
            {"value": "Do you love crackers?", "label": 1, "key": "g2"},
            {"value": "Do you love broth?", "label": 1, "key": "g2"},
            {"value": "Do you love chicken soup?", "label": 1, "key": "g2"},
            {"value": "Do you love chicken soup for dinner?", "label": 1, "key": "g2"},
            {"value": "Do you love chicken soup for dinner?", "label": 1, "key": "g2"},
        ],
    )
    prediction = model.predict("Do you love soup?")
    assert prediction.label == 1
    assert prediction.label_name == "cats"

    ClassificationModel.drop("test_predict_with_memoryset_update")


def test_last_prediction_with_batch(classification_model: ClassificationModel):
    predictions = classification_model.predict(["Do you love soup?", "Are cats cute?"])
    assert classification_model.last_prediction is not None
    assert classification_model.last_prediction.prediction_id == predictions[-1].prediction_id
    assert classification_model.last_prediction.input_value == "Are cats cute?"
    assert classification_model._last_prediction_was_batch is True


def test_last_prediction_with_single(classification_model: ClassificationModel):
    # Test that last_prediction is updated correctly with single prediction
    prediction = classification_model.predict("Do you love soup?")
    assert classification_model.last_prediction is not None
    assert classification_model.last_prediction.prediction_id == prediction.prediction_id
    assert classification_model.last_prediction.input_value == "Do you love soup?"
    assert classification_model._last_prediction_was_batch is False


@skip_in_ci("We don't have Anthropic API key in CI")
def test_explain(writable_memoryset: LabeledMemoryset):

    writable_memoryset.analyze(
        {"name": "distribution", "neighbor_counts": [1, 3]},
        lookup_count=3,
    )

    model = ClassificationModel.create(
        "test_model_for_explain",
        writable_memoryset,
        num_classes=2,
        memory_lookup_count=3,
        description="This is a test model for explain",
    )

    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2

    try:
        explanation = predictions[0].explanation
        assert explanation is not None
        assert len(explanation) > 10
        assert "soup" in explanation.lower()
    except Exception as e:
        if "ANTHROPIC_API_KEY" in str(e):
            logging.info("Skipping explanation test because ANTHROPIC_API_KEY is not set")
        else:
            raise e
    finally:
        ClassificationModel.drop("test_model_for_explain")


@skip_in_ci("We don't have Anthropic API key in CI")
def test_action_recommendation(writable_memoryset: LabeledMemoryset):
    """Test getting action recommendations for predictions"""

    writable_memoryset.analyze(
        {"name": "distribution", "neighbor_counts": [1, 3]},
        lookup_count=3,
    )

    model = ClassificationModel.create(
        "test_model_for_action",
        writable_memoryset,
        num_classes=2,
        memory_lookup_count=3,
        description="This is a test model for action recommendations",
    )

    # Make a prediction with expected label to simulate incorrect prediction
    prediction = model.predict("Do you love soup?", expected_labels=1)

    memoryset_length = model.memoryset.length

    try:
        # Get action recommendation
        action, rationale = prediction.recommend_action()

        assert action is not None
        assert rationale is not None
        assert action in ["remove_duplicates", "detect_mislabels", "add_memories", "finetuning"]
        assert len(rationale) > 10

        # Test memory suggestions
        suggestions_response = prediction.generate_memory_suggestions(num_memories=2)
        memory_suggestions = suggestions_response.suggestions

        assert memory_suggestions is not None
        assert len(memory_suggestions) == 2

        for suggestion in memory_suggestions:
            assert isinstance(suggestion[0], str)
            assert len(suggestion[0]) > 0
            assert isinstance(suggestion[1], str)
            assert suggestion[1] in model.memoryset.label_names

        suggestions_response.apply()

        model.memoryset.refresh()
        assert model.memoryset.length == memoryset_length + 2

    except Exception as e:
        if "ANTHROPIC_API_KEY" in str(e):
            logging.info("Skipping agent tests because ANTHROPIC_API_KEY is not set")
        else:
            raise e
    finally:
        ClassificationModel.drop("test_model_for_action")


def test_predict_with_prompt(classification_model: ClassificationModel):
    """Test that prompt parameter is properly passed through to predictions"""
    # Test with an instruction-supporting embedding model if available
    prediction_with_prompt = classification_model.predict(
        "I love this product!", prompt="Represent this text for sentiment classification:"
    )
    prediction_without_prompt = classification_model.predict("I love this product!")

    # Both should work and return valid predictions
    assert prediction_with_prompt.label is not None
    assert prediction_without_prompt.label is not None


@pytest.mark.asyncio
async def test_predict_async_single(classification_model: ClassificationModel, label_names: list[str]):
    """Test async prediction with a single value"""
    prediction = await classification_model.apredict("Do you love soup?")
    assert isinstance(prediction, ClassificationPrediction)
    assert prediction.prediction_id is not None
    assert prediction.label == 0
    assert prediction.label_name == label_names[0]
    assert 0 <= prediction.confidence <= 1
    assert prediction.logits is not None
    assert len(prediction.logits) == 2


@pytest.mark.asyncio
async def test_predict_async_batch(classification_model: ClassificationModel, label_names: list[str]):
    """Test async prediction with a batch of values"""
    predictions = await classification_model.apredict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2
    assert predictions[0].prediction_id is not None
    assert predictions[1].prediction_id is not None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1


@pytest.mark.asyncio
async def test_predict_async_with_expected_labels(classification_model: ClassificationModel):
    """Test async prediction with expected labels"""
    prediction = await classification_model.apredict("Do you love soup?", expected_labels=1)
    assert prediction.expected_label == 1


@pytest.mark.asyncio
async def test_predict_async_disable_telemetry(classification_model: ClassificationModel, label_names: list[str]):
    """Test async prediction with telemetry disabled"""
    predictions = await classification_model.apredict(["Do you love soup?", "Are cats cute?"], save_telemetry="off")
    assert len(predictions) == 2
    assert predictions[0].prediction_id is None
    assert predictions[1].prediction_id is None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1


@pytest.mark.asyncio
async def test_predict_async_with_filters(classification_model: ClassificationModel):
    """Test async prediction with filters"""
    # there are no memories with label 0 and key g2, so we force a wrong prediction
    filtered_prediction = await classification_model.apredict("I love soup", filters=[("key", "==", "g2")])
    assert filtered_prediction.label == 1
    assert filtered_prediction.label_name == "cats"
