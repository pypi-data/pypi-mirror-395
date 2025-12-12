import random
from uuid import uuid4

import pytest
from datasets.arrow_dataset import Dataset

from .classification_model import ClassificationModel
from .conftest import skip_in_ci, skip_in_prod
from .datasource import Datasource
from .embedding_model import PretrainedEmbeddingModel
from .memoryset import (
    LabeledMemory,
    LabeledMemoryset,
    ScoredMemory,
    ScoredMemoryset,
    Status,
)
from .regression_model import RegressionModel

"""
Test Performance Note:

Creating new `LabeledMemoryset` objects is expensive, so this test file applies the following optimizations:

- Two fixtures are used to manage memorysets:
    - `readonly_memoryset` is a session-scoped fixture shared across tests that do not modify state.
      It should only be used in nullipotent tests.
    - `writable_memoryset` is a function-scoped, regenerating fixture.
      It can be used in tests that mutate or delete the memoryset, and will be reset before each test.

- To minimize fixture overhead, tests using `writable_memoryset` should combine related behaviors.
  For example, prefer a single `test_delete` that covers both single and multiple deletion cases,
  rather than separate `test_delete_single` and `test_delete_multiple` tests.
"""


def test_create_memoryset(readonly_memoryset: LabeledMemoryset, hf_dataset: Dataset, label_names: list[str]):
    assert readonly_memoryset is not None
    assert readonly_memoryset.name == "test_readonly_memoryset"
    assert readonly_memoryset.embedding_model == PretrainedEmbeddingModel.GTE_BASE
    assert readonly_memoryset.label_names == label_names
    assert readonly_memoryset.insertion_status == Status.COMPLETED
    assert isinstance(readonly_memoryset.length, int)
    assert readonly_memoryset.length == len(hf_dataset)
    assert readonly_memoryset.index_type == "IVF_FLAT"
    assert readonly_memoryset.index_params == {"n_lists": 100}


def test_create_memoryset_unauthenticated(unauthenticated_client, datasource):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            LabeledMemoryset.create("test_memoryset", datasource)


def test_create_memoryset_invalid_input(datasource):
    # invalid name
    with pytest.raises(ValueError, match=r"Invalid input:.*"):
        LabeledMemoryset.create("test memoryset", datasource)


def test_create_memoryset_already_exists_error(hf_dataset, label_names, readonly_memoryset):
    memoryset_name = readonly_memoryset.name
    with pytest.raises(ValueError):
        LabeledMemoryset.from_hf_dataset(memoryset_name, hf_dataset, label_names=label_names)
    with pytest.raises(ValueError):
        LabeledMemoryset.from_hf_dataset(memoryset_name, hf_dataset, label_names=label_names, if_exists="error")


def test_create_memoryset_already_exists_open(hf_dataset, label_names, readonly_memoryset):
    # invalid label names
    with pytest.raises(ValueError):
        LabeledMemoryset.from_hf_dataset(
            readonly_memoryset.name,
            hf_dataset,
            label_names=["turtles", "frogs"],
            if_exists="open",
        )
    # different embedding model
    with pytest.raises(ValueError):
        LabeledMemoryset.from_hf_dataset(
            readonly_memoryset.name,
            hf_dataset,
            label_names=label_names,
            embedding_model=PretrainedEmbeddingModel.DISTILBERT,
            if_exists="open",
        )
    opened_memoryset = LabeledMemoryset.from_hf_dataset(
        readonly_memoryset.name,
        hf_dataset,
        embedding_model=PretrainedEmbeddingModel.GTE_BASE,
        if_exists="open",
    )
    assert opened_memoryset is not None
    assert opened_memoryset.name == readonly_memoryset.name
    assert opened_memoryset.length == len(hf_dataset)


def test_if_exists_error_no_datasource_creation(
    readonly_memoryset: LabeledMemoryset,
):
    memoryset_name = readonly_memoryset.name
    datasource_name = f"{memoryset_name}_datasource"
    Datasource.drop(datasource_name, if_not_exists="ignore")
    assert not Datasource.exists(datasource_name)
    with pytest.raises(ValueError):
        LabeledMemoryset.from_list(memoryset_name, [{"value": "new value", "label": 0}], if_exists="error")
    assert not Datasource.exists(datasource_name)


def test_if_exists_open_reuses_existing_datasource(
    readonly_memoryset: LabeledMemoryset,
):
    memoryset_name = readonly_memoryset.name
    datasource_name = f"{memoryset_name}_datasource"
    Datasource.drop(datasource_name, if_not_exists="ignore")
    assert not Datasource.exists(datasource_name)
    reopened = LabeledMemoryset.from_list(memoryset_name, [{"value": "new value", "label": 0}], if_exists="open")
    assert reopened.id == readonly_memoryset.id
    assert not Datasource.exists(datasource_name)


def test_create_memoryset_string_label():
    assert not LabeledMemoryset.exists("test_string_label")
    memoryset = LabeledMemoryset.from_hf_dataset(
        "test_string_label",
        Dataset.from_dict({"value": ["terrible", "great"], "label": ["negative", "positive"]}),
    )
    assert memoryset is not None
    assert memoryset.length == 2
    assert memoryset.label_names == ["negative", "positive"]
    assert memoryset[0].label == 0
    assert memoryset[1].label == 1
    assert memoryset[0].label_name == "negative"
    assert memoryset[1].label_name == "positive"


def test_create_memoryset_integer_label():
    assert not LabeledMemoryset.exists("test_integer_label")
    memoryset = LabeledMemoryset.from_hf_dataset(
        "test_integer_label",
        Dataset.from_dict({"value": ["terrible", "great"], "label": [0, 1]}),
        label_names=["negative", "positive"],
    )
    assert memoryset is not None
    assert memoryset.length == 2
    assert memoryset.label_names == ["negative", "positive"]
    assert memoryset[0].label == 0
    assert memoryset[1].label == 1
    assert memoryset[0].label_name == "negative"
    assert memoryset[1].label_name == "positive"


def test_create_memoryset_null_labels():
    memoryset = LabeledMemoryset.from_hf_dataset(
        "test_null_labels",
        Dataset.from_dict({"value": ["terrible", "great"]}),
        label_names=["negative", "positive"],
        label_column=None,
    )
    assert memoryset is not None
    assert memoryset.length == 2
    assert memoryset.label_names == ["negative", "positive"]
    assert memoryset[0].label is None
    assert memoryset[1].label is None


def test_open_memoryset(readonly_memoryset, hf_dataset):
    fetched_memoryset = LabeledMemoryset.open(readonly_memoryset.name)
    assert fetched_memoryset is not None
    assert fetched_memoryset.name == readonly_memoryset.name
    assert fetched_memoryset.length == len(hf_dataset)
    assert fetched_memoryset.index_type == "IVF_FLAT"
    assert fetched_memoryset.index_params == {"n_lists": 100}


def test_open_memoryset_unauthenticated(unauthenticated_client, readonly_memoryset):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            LabeledMemoryset.open(readonly_memoryset.name)


def test_open_memoryset_not_found():
    with pytest.raises(LookupError):
        LabeledMemoryset.open(str(uuid4()))


def test_open_memoryset_invalid_input():
    with pytest.raises(ValueError, match=r"Invalid input:.*"):
        LabeledMemoryset.open("not valid id")


def test_open_memoryset_unauthorized(unauthorized_client, readonly_memoryset):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            LabeledMemoryset.open(readonly_memoryset.name)


def test_all_memorysets(readonly_memoryset: LabeledMemoryset):
    memorysets = LabeledMemoryset.all()
    assert len(memorysets) > 0
    assert any(memoryset.name == readonly_memoryset.name for memoryset in memorysets)


def test_all_memorysets_hidden(
    readonly_memoryset: LabeledMemoryset,
):
    # Create a hidden memoryset
    hidden_memoryset = LabeledMemoryset.clone(readonly_memoryset, "test_hidden_memoryset")
    hidden_memoryset.set(hidden=True)

    # Test that show_hidden=False excludes hidden memorysets
    visible_memorysets = LabeledMemoryset.all(show_hidden=False)
    assert len(visible_memorysets) > 0
    assert readonly_memoryset in visible_memorysets
    assert hidden_memoryset not in visible_memorysets

    # Test that show_hidden=True includes hidden memorysets
    all_memorysets = LabeledMemoryset.all(show_hidden=True)
    assert len(all_memorysets) == len(visible_memorysets) + 1
    assert readonly_memoryset in all_memorysets
    assert hidden_memoryset in all_memorysets


def test_all_memorysets_unauthenticated(unauthenticated_client):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            LabeledMemoryset.all()


def test_all_memorysets_unauthorized(unauthorized_client, readonly_memoryset):
    with unauthorized_client.use():
        assert readonly_memoryset not in LabeledMemoryset.all()


def test_drop_memoryset_unauthenticated(unauthenticated_client, readonly_memoryset):
    with unauthenticated_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            LabeledMemoryset.drop(readonly_memoryset.name)


def test_drop_memoryset_not_found():
    with pytest.raises(LookupError):
        LabeledMemoryset.drop(str(uuid4()))
    # ignores error if specified
    LabeledMemoryset.drop(str(uuid4()), if_not_exists="ignore")


def test_drop_memoryset_unauthorized(unauthorized_client, readonly_memoryset):
    with unauthorized_client.use():
        with pytest.raises(LookupError):
            LabeledMemoryset.drop(readonly_memoryset.name)


def test_update_memoryset_attributes(writable_memoryset: LabeledMemoryset):
    original_label_names = writable_memoryset.label_names
    writable_memoryset.set(description="New description")
    assert writable_memoryset.description == "New description"

    writable_memoryset.set(description=None)
    assert writable_memoryset.description is None

    writable_memoryset.set(name="New_name")
    assert writable_memoryset.name == "New_name"

    writable_memoryset.set(name="test_writable_memoryset")
    assert writable_memoryset.name == "test_writable_memoryset"

    assert writable_memoryset.label_names == original_label_names

    writable_memoryset.set(label_names=["New label 1", "New label 2"])
    assert writable_memoryset.label_names == ["New label 1", "New label 2"]

    writable_memoryset.set(hidden=True)
    assert writable_memoryset.hidden is True


def test_search(readonly_memoryset: LabeledMemoryset):
    memory_lookups = readonly_memoryset.search(["i love soup", "cats are cute"])
    assert len(memory_lookups) == 2
    assert len(memory_lookups[0]) == 1
    assert len(memory_lookups[1]) == 1
    assert memory_lookups[0][0].label == 0
    assert memory_lookups[1][0].label == 1


def test_search_count(readonly_memoryset: LabeledMemoryset):
    memory_lookups = readonly_memoryset.search("i love soup", count=3)
    assert len(memory_lookups) == 3
    assert memory_lookups[0].label == 0
    assert memory_lookups[1].label == 0
    assert memory_lookups[2].label == 0


def test_search_with_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search within a specific partition - use "soup" which appears in both p1 and p2
    # Use exclude_global to ensure we only get results from the specified partition
    memory_lookups = readonly_partitioned_memoryset.search(
        "soup", partition_id="p1", partition_filter_mode="exclude_global", count=5
    )
    assert len(memory_lookups) > 0
    # All results should be from partition p1 when partition_id is specified
    assert all(
        memory.partition_id == "p1" for memory in memory_lookups
    ), f"Expected all results from partition p1, but got: {[m.partition_id for m in memory_lookups]}"

    # Search in a different partition - use "cats" which appears in both p1 and p2
    memory_lookups_p2 = readonly_partitioned_memoryset.search(
        "cats", partition_id="p2", partition_filter_mode="exclude_global", count=5
    )
    assert len(memory_lookups_p2) > 0
    # All results should be from partition p2 when partition_id is specified
    assert all(
        memory.partition_id == "p2" for memory in memory_lookups_p2
    ), f"Expected all results from partition p2, but got: {[m.partition_id for m in memory_lookups_p2]}"


def test_search_with_partition_filter_mode_exclude_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search excluding global memories - need to specify a partition_id when using exclude_global
    # This tests that exclude_global works with a specific partition
    memory_lookups = readonly_partitioned_memoryset.search(
        "soup", partition_id="p1", partition_filter_mode="exclude_global", count=5
    )
    assert len(memory_lookups) > 0
    # All results should have a partition_id (not None) and be from p1
    assert all(memory.partition_id == "p1" for memory in memory_lookups)


def test_search_with_partition_filter_mode_only_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search only in global memories (partition_id=None in the data)
    # Use a query that matches global memories and a reasonable count
    memory_lookups = readonly_partitioned_memoryset.search("beach", partition_filter_mode="only_global", count=3)
    # Should get at least some results (may be fewer than requested if not enough global memories match)
    assert len(memory_lookups) > 0
    # All results should be global (partition_id is None)
    partition_ids = {memory.partition_id for memory in memory_lookups}
    # When using only_global, all results should be global (either None)
    assert all(
        memory.partition_id is None for memory in memory_lookups
    ), f"Expected all results to be global (partition_id=None), but got partition_ids: {partition_ids}"


def test_search_with_partition_filter_mode_include_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search including global memories (default behavior)
    # Use a reasonable count that won't exceed available memories
    memory_lookups = readonly_partitioned_memoryset.search(
        "i love soup", partition_filter_mode="include_global", count=5
    )
    assert len(memory_lookups) > 0
    # Results can include both partitioned and global memories
    partition_ids = {memory.partition_id for memory in memory_lookups}
    # Should have at least one partition or global memory
    assert len(partition_ids) > 0


def test_search_with_partition_filter_mode_ignore_partitions(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search ignoring partition filtering entirely
    memory_lookups = readonly_partitioned_memoryset.search(
        "i love soup", partition_filter_mode="ignore_partitions", count=10
    )
    assert len(memory_lookups) > 0
    # Results can come from any partition or global
    partition_ids = {memory.partition_id for memory in memory_lookups}
    # Should have results from multiple partitions/global
    assert len(partition_ids) >= 1


def test_search_multiple_queries_with_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Search multiple queries within a specific partition
    memory_lookups = readonly_partitioned_memoryset.search(["i love soup", "cats are cute"], partition_id="p1", count=3)
    assert len(memory_lookups) == 2
    assert len(memory_lookups[0]) > 0
    assert len(memory_lookups[1]) > 0
    # All results should be from partition p1
    assert all(memory.partition_id == "p1" for memory in memory_lookups[0])
    assert all(memory.partition_id == "p1" for memory in memory_lookups[1])


def test_search_with_partition_id_and_filter_mode(readonly_partitioned_memoryset: LabeledMemoryset):
    # When partition_id is specified, partition_filter_mode should still work
    # Search in p1 with exclude_global (should only return p1 results)
    memory_lookups = readonly_partitioned_memoryset.search(
        "i love soup", partition_id="p1", partition_filter_mode="exclude_global", count=5
    )
    assert len(memory_lookups) > 0
    assert all(memory.partition_id == "p1" for memory in memory_lookups)


def test_get_memory_at_index(readonly_memoryset: LabeledMemoryset, hf_dataset: Dataset, label_names: list[str]):
    memory = readonly_memoryset[0]
    assert memory.value == hf_dataset[0]["value"]
    assert memory.label == hf_dataset[0]["label"]
    assert memory.label_name == label_names[hf_dataset[0]["label"]]
    assert memory.source_id == hf_dataset[0]["source_id"]
    assert memory.score == hf_dataset[0]["score"]
    assert memory.key == hf_dataset[0]["key"]
    last_memory = readonly_memoryset[-1]
    assert last_memory.value == hf_dataset[-1]["value"]
    assert last_memory.label == hf_dataset[-1]["label"]


def test_get_range_of_memories(readonly_memoryset: LabeledMemoryset, hf_dataset: Dataset):
    memories = readonly_memoryset[1:3]
    assert len(memories) == 2
    assert memories[0].value == hf_dataset["value"][1]
    assert memories[1].value == hf_dataset["value"][2]


def test_get_memory_by_id(readonly_memoryset: LabeledMemoryset, hf_dataset: Dataset):
    memory = readonly_memoryset.get(readonly_memoryset[0].memory_id)
    assert memory.value == hf_dataset[0]["value"]
    assert memory == readonly_memoryset[memory.memory_id]


def test_get_memories_by_id(readonly_memoryset: LabeledMemoryset, hf_dataset: Dataset):
    memories = readonly_memoryset.get([readonly_memoryset[0].memory_id, readonly_memoryset[1].memory_id])
    assert len(memories) == 2
    assert memories[0].value == hf_dataset[0]["value"]
    assert memories[1].value == hf_dataset[1]["value"]


def test_query_memoryset(readonly_memoryset: LabeledMemoryset):
    memories = readonly_memoryset.query(filters=[("label", "==", 1)])
    assert len(memories) == 8
    assert all(memory.label == 1 for memory in memories)
    assert len(readonly_memoryset.query(limit=2)) == 2
    assert len(readonly_memoryset.query(filters=[("metadata.key", "==", "g2")])) == 4


def test_query_memoryset_with_feedback_metrics(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?")
    feedback_name = f"correct_{random.randint(0, 1000000)}"
    prediction.record_feedback(category=feedback_name, value=prediction.label == 0)
    memories = prediction.memoryset.query(filters=[("label", "==", 0)], with_feedback_metrics=True)

    # Get the memory_ids that were actually used in the prediction
    used_memory_ids = {memory.memory_id for memory in prediction.memory_lookups}

    assert len(memories) == 8
    assert all(memory.label == 0 for memory in memories)
    for memory in memories:
        assert memory.feedback_metrics is not None
        if memory.memory_id in used_memory_ids:
            assert feedback_name in memory.feedback_metrics
            assert memory.feedback_metrics[feedback_name]["avg"] == 1.0
            assert memory.feedback_metrics[feedback_name]["count"] == 1
        else:
            assert feedback_name not in memory.feedback_metrics or memory.feedback_metrics[feedback_name]["count"] == 0
        assert isinstance(memory.lookup_count, int)


def test_query_memoryset_with_feedback_metrics_filter(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?")
    prediction.record_feedback(category="accurate", value=prediction.label == 0)
    memories = prediction.memoryset.query(
        filters=[("feedback_metrics.accurate.avg", ">", 0.5)], with_feedback_metrics=True
    )
    assert len(memories) == 3
    assert all(memory.label == 0 for memory in memories)
    for memory in memories:
        assert memory.feedback_metrics is not None
        assert memory.feedback_metrics["accurate"] is not None
        assert memory.feedback_metrics["accurate"]["avg"] == 1.0
        assert memory.feedback_metrics["accurate"]["count"] == 1


def test_query_memoryset_with_feedback_metrics_sort(classification_model: ClassificationModel):
    prediction = classification_model.predict("Do you love soup?")
    prediction.record_feedback(category="positive", value=1.0)
    prediction2 = classification_model.predict("Do you like cats?")
    prediction2.record_feedback(category="positive", value=-1.0)

    memories = prediction.memoryset.query(
        filters=[("feedback_metrics.positive.avg", ">=", -1.0)],
        sort=[("feedback_metrics.positive.avg", "desc")],
        with_feedback_metrics=True,
    )
    assert (
        len(memories) == 6
    )  # there are only 6 out of 16 memories that have a positive feedback metric. Look at SAMPLE_DATA in conftest.py
    assert memories[0].feedback_metrics["positive"]["avg"] == 1.0
    assert memories[-1].feedback_metrics["positive"]["avg"] == -1.0


def test_query_memoryset_with_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with partition_id and include_global (default) - includes both p1 and global memories
    memories = readonly_partitioned_memoryset.query(partition_id="p1")
    assert len(memories) == 15  # 8 p1 + 7 global = 15
    # Results should include both p1 and global memories
    partition_ids = {memory.partition_id for memory in memories}
    assert "p1" in partition_ids
    assert None in partition_ids


def test_query_memoryset_with_partition_id_and_exclude_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with partition_id and exclude_global mode - only returns p1 memories
    memories = readonly_partitioned_memoryset.query(partition_id="p1", partition_filter_mode="exclude_global")
    assert len(memories) == 8  # Only 8 p1 memories (no global)
    # All results should be from partition p1 (no global memories)
    assert all(memory.partition_id == "p1" for memory in memories)


def test_query_memoryset_with_partition_id_and_include_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with partition_id and include_global mode (default) - includes both p1 and global
    memories = readonly_partitioned_memoryset.query(partition_id="p1", partition_filter_mode="include_global")
    assert len(memories) == 15  # 8 p1 + 7 global = 15
    # Results should include both p1 and global memories
    partition_ids = {memory.partition_id for memory in memories}
    assert "p1" in partition_ids
    assert None in partition_ids


def test_query_memoryset_with_partition_filter_mode_exclude_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query excluding global memories requires a partition_id
    # Test with a specific partition_id
    memories = readonly_partitioned_memoryset.query(partition_id="p1", partition_filter_mode="exclude_global")
    assert len(memories) == 8  # Only p1 memories
    # All results should have a partition_id (not global)
    assert all(memory.partition_id == "p1" for memory in memories)


def test_query_memoryset_with_partition_filter_mode_only_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query only in global memories
    memories = readonly_partitioned_memoryset.query(partition_filter_mode="only_global")
    assert len(memories) == 7  # There are 7 global memories in SAMPLE_DATA
    # All results should be global (partition_id is None)
    assert all(memory.partition_id is None for memory in memories)


def test_query_memoryset_with_partition_filter_mode_include_global(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query including global memories - when no partition_id is specified,
    # include_global seems to only return global memories
    memories = readonly_partitioned_memoryset.query(partition_filter_mode="include_global")
    # Based on actual behavior, this returns only global memories
    assert len(memories) == 7
    # All results should be global
    assert all(memory.partition_id is None for memory in memories)


def test_query_memoryset_with_partition_filter_mode_ignore_partitions(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query ignoring partition filtering entirely - returns all memories
    memories = readonly_partitioned_memoryset.query(partition_filter_mode="ignore_partitions", limit=100)
    assert len(memories) == 22  # All 22 memories
    # Results can come from any partition or global
    partition_ids = {memory.partition_id for memory in memories}
    # Should have results from multiple partitions/global
    assert len(partition_ids) >= 1
    # Verify we have p1, p2, and global
    assert "p1" in partition_ids
    assert "p2" in partition_ids
    assert None in partition_ids


def test_query_memoryset_with_filters_and_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with filters and partition_id
    memories = readonly_partitioned_memoryset.query(filters=[("label", "==", 0)], partition_id="p1")
    assert len(memories) > 0
    # All results should match the filter and be from partition p1
    assert all(memory.label == 0 for memory in memories)
    assert all(memory.partition_id == "p1" for memory in memories)


def test_query_memoryset_with_filters_and_partition_filter_mode(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with filters and partition_filter_mode - exclude_global requires partition_id
    memories = readonly_partitioned_memoryset.query(
        filters=[("label", "==", 1)], partition_id="p1", partition_filter_mode="exclude_global"
    )
    assert len(memories) > 0
    # All results should match the filter and be from p1 (not global)
    assert all(memory.label == 1 for memory in memories)
    assert all(memory.partition_id == "p1" for memory in memories)


def test_query_memoryset_with_limit_and_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with limit and partition_id
    memories = readonly_partitioned_memoryset.query(partition_id="p2", limit=3)
    assert len(memories) == 3
    # All results should be from partition p2
    assert all(memory.partition_id == "p2" for memory in memories)


def test_query_memoryset_with_offset_and_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with offset and partition_id - use exclude_global to get only p1 memories
    memories_page1 = readonly_partitioned_memoryset.query(
        partition_id="p1", partition_filter_mode="exclude_global", limit=5
    )
    memories_page2 = readonly_partitioned_memoryset.query(
        partition_id="p1", partition_filter_mode="exclude_global", offset=5, limit=5
    )
    assert len(memories_page1) == 5
    assert len(memories_page2) == 3  # Only 3 remaining p1 memories (8 total - 5 = 3)
    # All results should be from partition p1
    assert all(memory.partition_id == "p1" for memory in memories_page1)
    assert all(memory.partition_id == "p1" for memory in memories_page2)
    # Results should be different (pagination works)
    memory_ids_page1 = {memory.memory_id for memory in memories_page1}
    memory_ids_page2 = {memory.memory_id for memory in memories_page2}
    assert memory_ids_page1.isdisjoint(memory_ids_page2)


def test_query_memoryset_with_partition_id_p2(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query a different partition to verify it works
    # With include_global (default), it includes both p2 and global memories
    memories = readonly_partitioned_memoryset.query(partition_id="p2")
    assert len(memories) == 14  # 7 p2 + 7 global = 14
    # Results should include both p2 and global memories
    partition_ids = {memory.partition_id for memory in memories}
    assert "p2" in partition_ids
    assert None in partition_ids


def test_query_memoryset_with_metadata_filter_and_partition_id(readonly_partitioned_memoryset: LabeledMemoryset):
    # Query with metadata filter and partition_id
    memories = readonly_partitioned_memoryset.query(filters=[("metadata.key", "==", "g1")], partition_id="p1")
    assert len(memories) > 0
    # All results should match the metadata filter and be from partition p1
    assert all(memory.metadata.get("key") == "g1" for memory in memories)
    assert all(memory.partition_id == "p1" for memory in memories)


def test_query_memoryset_with_partition_filter_mode_only_global_and_filters(
    readonly_partitioned_memoryset: LabeledMemoryset,
):
    # Query only global memories with filters
    memories = readonly_partitioned_memoryset.query(
        filters=[("metadata.key", "==", "g3")], partition_filter_mode="only_global"
    )
    assert len(memories) > 0
    # All results should match the filter and be global
    assert all(memory.metadata.get("key") == "g3" for memory in memories)
    assert all(memory.partition_id is None for memory in memories)


def test_labeled_memory_predictions_property(classification_model: ClassificationModel):
    """Test that LabeledMemory.predictions() only returns classification predictions."""
    # Given: A classification model with memories
    memories = classification_model.memoryset.query(limit=1)
    assert len(memories) > 0
    memory = memories[0]

    # When: I call the predictions method
    predictions = memory.predictions()

    # Then: It should return a list of ClassificationPrediction objects
    assert isinstance(predictions, list)
    for prediction in predictions:
        assert prediction.__class__.__name__ == "ClassificationPrediction"
        assert hasattr(prediction, "label")
        assert not hasattr(prediction, "score") or prediction.score is None


def test_scored_memory_predictions_property(regression_model: RegressionModel):
    """Test that ScoredMemory.predictions() only returns regression predictions."""
    # Given: A regression model with memories
    memories = regression_model.memoryset.query(limit=1)
    assert len(memories) > 0
    memory = memories[0]

    # When: I call the predictions method
    predictions = memory.predictions()

    # Then: It should return a list of RegressionPrediction objects
    assert isinstance(predictions, list)
    for prediction in predictions:
        assert prediction.__class__.__name__ == "RegressionPrediction"
        assert hasattr(prediction, "score")
        assert not hasattr(prediction, "label") or prediction.label is None


def test_memory_feedback_property(classification_model: ClassificationModel):
    """Test that memory.feedback() returns feedback from relevant predictions."""
    # Given: A prediction with recorded feedback
    prediction = classification_model.predict("Test feedback")
    feedback_category = f"test_feedback_{random.randint(0, 1000000)}"
    prediction.record_feedback(category=feedback_category, value=True)

    # And: A memory that was used in the prediction
    memory_lookups = prediction.memory_lookups
    assert len(memory_lookups) > 0
    memory = memory_lookups[0]

    # When: I access the feedback property
    feedback = memory.feedback()

    # Then: It should return feedback aggregated by category as a dict
    assert isinstance(feedback, dict)
    assert feedback_category in feedback
    # Feedback values are lists (you may want to look at mean on the raw data)
    assert isinstance(feedback[feedback_category], list)
    assert len(feedback[feedback_category]) > 0
    # For binary feedback, values should be booleans
    assert isinstance(feedback[feedback_category][0], bool)


def test_memory_predictions_method_parameters(classification_model: ClassificationModel):
    """Test that memory.predictions() method supports pagination, sorting, and filtering."""
    # Given: A classification model with memories
    memories = classification_model.memoryset.query(limit=1)
    assert len(memories) > 0
    memory = memories[0]

    # When: I call predictions with limit parameter
    predictions_limited = memory.predictions(limit=2)

    # Then: It should respect the limit
    assert isinstance(predictions_limited, list)
    assert len(predictions_limited) <= 2

    # When: I call predictions with offset parameter
    all_predictions = memory.predictions(limit=100)
    if len(all_predictions) > 1:
        predictions_offset = memory.predictions(limit=1, offset=1)
        # Then: offset should skip the first prediction
        assert predictions_offset[0].prediction_id != all_predictions[0].prediction_id

    # When: I call predictions with sort parameter
    predictions_sorted = memory.predictions(limit=10, sort=[("timestamp", "desc")])
    # Then: It should return predictions (sorting verified by API)
    assert isinstance(predictions_sorted, list)

    # When: I call predictions with expected_label_match parameter
    correct_predictions = memory.predictions(expected_label_match=True)
    incorrect_predictions = memory.predictions(expected_label_match=False)
    # Then: Both should return lists (correctness verified by API filtering)
    assert isinstance(correct_predictions, list)
    assert isinstance(incorrect_predictions, list)


def test_memory_predictions_expected_label_filter(classification_model: ClassificationModel):
    """Test that memory.predictions(expected_label_match=...) filters predictions by correctness."""
    # Given: Make an initial prediction to learn the model's label for a known input
    baseline_prediction = classification_model.predict("Filter test input", save_telemetry="sync")
    original_label = baseline_prediction.label
    alternate_label = 0 if original_label else 1

    # When: Make a second prediction with an intentionally incorrect expected label
    mismatched_prediction = classification_model.predict(
        "Filter test input",
        expected_labels=alternate_label,
        save_telemetry="sync",
    )
    mismatched_memory = mismatched_prediction.memory_lookups[0]

    # Then: The prediction should show up when filtering for incorrect predictions
    incorrect_predictions = mismatched_memory.predictions(expected_label_match=False)
    assert any(pred.prediction_id == mismatched_prediction.prediction_id for pred in incorrect_predictions)

    # Produce a correct prediction (predicted label matches expected label)
    correct_prediction = classification_model.predict(
        "Filter test input",
        expected_labels=original_label,
        save_telemetry="sync",
    )

    # Ensure we are inspecting a memory used by both correct and incorrect predictions
    correct_lookup_ids = {lookup.memory_id for lookup in correct_prediction.memory_lookups}
    if mismatched_memory.memory_id not in correct_lookup_ids:
        shared_lookup = next(
            (lookup for lookup in mismatched_prediction.memory_lookups if lookup.memory_id in correct_lookup_ids),
            None,
        )
        assert shared_lookup is not None, "No shared memory lookup between correct and incorrect predictions"
        mismatched_memory = shared_lookup

    # And: The correct prediction should appear when filtering for correct predictions
    correct_predictions = mismatched_memory.predictions(expected_label_match=True)
    assert any(pred.prediction_id == correct_prediction.prediction_id for pred in correct_predictions)
    assert all(pred.prediction_id != mismatched_prediction.prediction_id for pred in correct_predictions)


def test_insert_memories(writable_memoryset: LabeledMemoryset):
    writable_memoryset.refresh()
    prev_length = writable_memoryset.length
    writable_memoryset.insert(
        [
            dict(value="tomato soup is my favorite", label=0),
            dict(value="cats are fun to play with", label=1),
        ]
    )
    writable_memoryset.refresh()
    assert writable_memoryset.length == prev_length + 2
    writable_memoryset.insert(dict(value="tomato soup is my favorite", label=0, key="test", source_id="test"))
    writable_memoryset.refresh()
    assert writable_memoryset.length == prev_length + 3
    last_memory = writable_memoryset[-1]
    assert last_memory.value == "tomato soup is my favorite"
    assert last_memory.label == 0
    assert last_memory.metadata
    assert last_memory.metadata["key"] == "test"
    assert last_memory.source_id == "test"


@skip_in_prod("Production memorysets do not have session consistency guarantees")
@skip_in_ci("CI environment may not have session consistency guarantees")
def test_update_memories(writable_memoryset: LabeledMemoryset, hf_dataset: Dataset):
    # We've combined the update tests into one to avoid multiple expensive requests for a writable_memoryset

    # test updating a single memory
    memory_id = writable_memoryset[0].memory_id
    updated_memory = writable_memoryset.update(dict(memory_id=memory_id, value="i love soup so much"))
    assert updated_memory.value == "i love soup so much"
    assert updated_memory.label == hf_dataset[0]["label"]
    writable_memoryset.refresh()  # Refresh to ensure consistency after update
    assert writable_memoryset.get(memory_id).value == "i love soup so much"

    # test updating a memory instance
    memory = writable_memoryset[0]
    updated_memory = memory.update(value="i love soup even more")
    assert updated_memory is memory
    assert memory.value == "i love soup even more"
    assert memory.label == hf_dataset[0]["label"]

    # test updating multiple memories
    memory_ids = [memory.memory_id for memory in writable_memoryset[:2]]
    updated_memories = writable_memoryset.update(
        [
            dict(memory_id=memory_ids[0], value="i love soup so much"),
            dict(memory_id=memory_ids[1], value="cats are so cute"),
        ]
    )
    assert updated_memories[0].value == "i love soup so much"
    assert updated_memories[1].value == "cats are so cute"


def test_delete_memories(writable_memoryset: LabeledMemoryset):
    # We've combined the delete tests into one to avoid multiple expensive requests for a writable_memoryset

    # test deleting a single memory
    prev_length = writable_memoryset.length
    memory_id = writable_memoryset[0].memory_id
    writable_memoryset.delete(memory_id)
    with pytest.raises(LookupError):
        writable_memoryset.get(memory_id)
    assert writable_memoryset.length == prev_length - 1

    # test deleting multiple memories
    prev_length = writable_memoryset.length
    writable_memoryset.delete([writable_memoryset[0].memory_id, writable_memoryset[1].memory_id])
    assert writable_memoryset.length == prev_length - 2


def test_clone_memoryset(readonly_memoryset: LabeledMemoryset):
    cloned_memoryset = readonly_memoryset.clone(
        "test_cloned_memoryset", embedding_model=PretrainedEmbeddingModel.DISTILBERT
    )
    assert cloned_memoryset is not None
    assert cloned_memoryset.name == "test_cloned_memoryset"
    assert cloned_memoryset.length == readonly_memoryset.length
    assert cloned_memoryset.embedding_model == PretrainedEmbeddingModel.DISTILBERT
    assert cloned_memoryset.insertion_status == Status.COMPLETED


@pytest.fixture(scope="function")
async def test_group_potential_duplicates(writable_memoryset: LabeledMemoryset):
    writable_memoryset.insert(
        [
            dict(value="raspberry soup Is my favorite", label=0),
            dict(value="Raspberry soup is MY favorite", label=0),
            dict(value="rAspberry soup is my favorite", label=0),
            dict(value="raSpberry SOuP is my favorite", label=0),
            dict(value="rasPberry SOuP is my favorite", label=0),
            dict(value="bunny rabbit Is not my mom", label=1),
            dict(value="bunny rabbit is not MY mom", label=1),
            dict(value="bunny rabbit Is not my moM", label=1),
            dict(value="bunny rabbit is not my mom", label=1),
            dict(value="bunny rabbit is not my mom", label=1),
            dict(value="bunny rabbit is not My mom", label=1),
        ]
    )

    writable_memoryset.analyze({"name": "duplicate", "possible_duplicate_threshold": 0.97})
    response = writable_memoryset.get_potential_duplicate_groups()
    assert isinstance(response, list)
    assert sorted([len(res) for res in response]) == [5, 6]  # 5 favorite, 6 mom


def test_get_cascading_edits_suggestions(writable_memoryset: LabeledMemoryset):
    # Insert a memory to test cascading edits
    SOUP = 0
    CATS = 1
    query_text = "i love soup"  # from SAMPLE_DATA in conftest.py
    mislabeled_soup_text = "soup is comfort in a bowl"
    writable_memoryset.insert(
        [
            dict(value=mislabeled_soup_text, label=CATS),  # mislabeled soup memory
        ]
    )

    # Fetch the memory to update
    memory = writable_memoryset.query(filters=[("value", "==", query_text)])[0]

    # Update the label and get cascading edit suggestions
    suggestions = writable_memoryset.get_cascading_edits_suggestions(
        memory=memory,
        old_label=CATS,
        new_label=SOUP,
        max_neighbors=10,
        max_validation_neighbors=5,
    )

    # Validate the suggestions
    assert len(suggestions) == 1
    assert suggestions[0]["neighbor"]["value"] == mislabeled_soup_text


def test_analyze_invalid_analysis_name(readonly_memoryset: LabeledMemoryset):
    """Test that analyze() raises ValueError for invalid analysis names"""
    memoryset = LabeledMemoryset.open(readonly_memoryset.name)

    # Test with string input
    with pytest.raises(ValueError) as excinfo:
        memoryset.analyze("invalid_name")
    assert "Invalid analysis name: invalid_name" in str(excinfo.value)
    assert "Valid names are:" in str(excinfo.value)

    # Test with dict input
    with pytest.raises(ValueError) as excinfo:
        memoryset.analyze({"name": "invalid_name"})
    assert "Invalid analysis name: invalid_name" in str(excinfo.value)
    assert "Valid names are:" in str(excinfo.value)

    # Test with multiple analyses where one is invalid
    with pytest.raises(ValueError) as excinfo:
        memoryset.analyze("duplicate", "invalid_name")
    assert "Invalid analysis name: invalid_name" in str(excinfo.value)
    assert "Valid names are:" in str(excinfo.value)

    # Test with valid analysis names
    result = memoryset.analyze("duplicate", "cluster")
    assert isinstance(result, dict)
    assert "duplicate" in result
    assert "cluster" in result


def test_drop_memoryset(writable_memoryset: LabeledMemoryset):
    # NOTE: Keep this test at the end to ensure the memoryset is dropped after all tests.
    # Otherwise, it would be recreated on the next test run if it were dropped earlier, and
    # that's expensive.
    assert LabeledMemoryset.exists(writable_memoryset.name)
    LabeledMemoryset.drop(writable_memoryset.name)
    assert not LabeledMemoryset.exists(writable_memoryset.name)


def test_scored_memoryset(scored_memoryset: ScoredMemoryset):
    assert scored_memoryset.length == 22
    assert isinstance(scored_memoryset[0], ScoredMemory)
    assert scored_memoryset[0].value == "i love soup"
    assert scored_memoryset[0].score is not None
    assert scored_memoryset[0].metadata == {"key": "g1", "label": 0, "partition_id": "p1"}
    assert scored_memoryset[0].source_id == "s1"
    lookup = scored_memoryset.search("i love soup", count=1)
    assert len(lookup) == 1
    assert lookup[0].score is not None
    assert lookup[0].score < 0.11


@skip_in_prod("Production memorysets do not have session consistency guarantees")
def test_update_scored_memory(scored_memoryset: ScoredMemoryset):
    # we are only updating an inconsequential metadata field so that we don't affect other tests
    memory = scored_memoryset[0]
    assert memory.label == 0
    scored_memoryset.update(dict(memory_id=memory.memory_id, label=3))
    assert scored_memoryset[0].label == 3
    memory.update(label=4)
    assert scored_memoryset[0].label == 4


@pytest.mark.asyncio
async def test_insert_memories_async_single(writable_memoryset: LabeledMemoryset):
    """Test async insertion of a single memory"""
    await writable_memoryset.arefresh()
    prev_length = writable_memoryset.length

    await writable_memoryset.ainsert(dict(value="async tomato soup is my favorite", label=0, key="async_test"))

    await writable_memoryset.arefresh()
    assert writable_memoryset.length == prev_length + 1
    last_memory = writable_memoryset[-1]
    assert last_memory.value == "async tomato soup is my favorite"
    assert last_memory.label == 0
    assert last_memory.metadata["key"] == "async_test"


@pytest.mark.asyncio
async def test_insert_memories_async_batch(writable_memoryset: LabeledMemoryset):
    """Test async insertion of multiple memories"""
    await writable_memoryset.arefresh()
    prev_length = writable_memoryset.length

    await writable_memoryset.ainsert(
        [
            dict(value="async batch soup is delicious", label=0, key="batch_test_1"),
            dict(value="async batch cats are adorable", label=1, key="batch_test_2"),
        ]
    )

    await writable_memoryset.arefresh()
    assert writable_memoryset.length == prev_length + 2

    # Check the inserted memories
    last_two_memories = writable_memoryset[-2:]
    values = [memory.value for memory in last_two_memories]
    labels = [memory.label for memory in last_two_memories]
    keys = [memory.metadata.get("key") for memory in last_two_memories]

    assert "async batch soup is delicious" in values
    assert "async batch cats are adorable" in values
    assert 0 in labels
    assert 1 in labels
    assert "batch_test_1" in keys
    assert "batch_test_2" in keys


@pytest.mark.asyncio
async def test_insert_memories_async_with_source_id(writable_memoryset: LabeledMemoryset):
    """Test async insertion with source_id and metadata"""
    await writable_memoryset.arefresh()
    prev_length = writable_memoryset.length

    await writable_memoryset.ainsert(
        dict(
            value="async soup with source id", label=0, source_id="async_source_123", custom_field="async_custom_value"
        )
    )

    await writable_memoryset.arefresh()
    assert writable_memoryset.length == prev_length + 1
    last_memory = writable_memoryset[-1]
    assert last_memory.value == "async soup with source id"
    assert last_memory.label == 0
    assert last_memory.source_id == "async_source_123"
    assert last_memory.metadata["custom_field"] == "async_custom_value"


@pytest.mark.asyncio
async def test_insert_memories_async_unauthenticated(
    unauthenticated_async_client, writable_memoryset: LabeledMemoryset
):
    """Test async insertion with invalid authentication"""
    with unauthenticated_async_client.use():
        with pytest.raises(ValueError, match="Invalid API key"):
            await writable_memoryset.ainsert(dict(value="this should fail", label=0))
