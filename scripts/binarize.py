# %%
import json
from typing import List, Dict, Literal, Set
from tqdm.autonotebook import tqdm

from faithbench_schema import FaithBenchBatch, FaithBenchSample, FaithBenchAnnotation, FaithBenchMetaInfo, FaithBenchLabel, FaithBenchTextPair

def load_one_batch(batch_id: int) -> List[FaithBenchSample]:
    with open(f"../data_for_release/batch_{batch_id}.json", "r") as f:
        batch: FaithBenchBatch = FaithBenchBatch.model_validate_json(f.read())
        batch: Dict = batch.model_dump(by_alias=True) # this returns a dict with the field names as the keys
        batch = batch["samples"]
        batch = [FaithBenchSample.model_validate(sample) for sample in batch]
    return batch

# %%
def get_sample_level_label(
        sample: FaithBenchSample, 
        aggregation_strategy: Literal["majority", "worst", "best"], 
        hallucinated_classes: List[FaithBenchLabel]
        ) -> str:

    # Step 1: collect the labels on each annotation in the sample
    labels: List[FaithBenchLabel] = []
    for annotation in sample.annotations:
        labels.extend(annotation.label) # each annotation can have multiple labels, e.g., ["Unwanted", "Unwanted_Intrinsic"]

    labels: Set[FaithBenchLabel] = set(labels)

    if len(labels) == 0:
        return 0 # the sample is consistent

    # Step 2: aggregate the per-annotation labels into a single sample-level label
    mapping_label_to_severity = {
        FaithBenchLabel.Benign: 1,       # least severe, best
        FaithBenchLabel.Questionable: 2, 
        FaithBenchLabel.Unwanted: 3,     # most severe, worst
        FaithBenchLabel.Unwanted_Intrinsic: 3, # most severe, worst
        FaithBenchLabel.Unwanted_Extrinsic: 3 # most severe, worst
    }

    mapping_severity_to_label = {number: label for label, number in mapping_label_to_severity.items()}

    # Step 3: Pool the labels into a single sample-level label after converting to severity scores
    labels: List[int] = [mapping_label_to_severity[label] for label in labels]

    if aggregation_strategy == "majority":
        sample_level_label: int = max(set(labels), key=labels.count)
    elif aggregation_strategy == "worst":
        sample_level_label: int = max(labels)
    elif aggregation_strategy == "best":
        sample_level_label: int = min(labels)

    # Step 4: Get a binary label
    sample_level_label: FaithBenchLabel = mapping_severity_to_label[sample_level_label] # map back to FaithBenchLabel
    sample_level_label = 0 if sample_level_label in hallucinated_classes else 1

    return sample_level_label

# %%
def binarize_sample(
    sample: FaithBenchSample, 
    aggregation_strategy: Literal["majority", "worst", "best"], 
    hallucinated_classes: List[FaithBenchLabel]
    ) -> FaithBenchTextPair:
    
    label = get_sample_level_label(sample, aggregation_strategy, hallucinated_classes)
    
    return FaithBenchTextPair(
        source=sample.source,
        summary=sample.summary,
        label=label
    )   

# %%
def binarize_batch(
    batch_id: int, 
    aggregation_strategy: Literal["majority", "worst", "best"], 
    hallucinated_classes: List[FaithBenchLabel]
    ) -> List[FaithBenchTextPair]:
    
    try: 
        batch_data = load_one_batch(batch_id)
        return [binarize_sample(sample, aggregation_strategy, hallucinated_classes) for sample in batch_data]
    except Exception as e:
        print (f"Error loading batch {batch_id}: {e}")
        return []

# %%
def gen_config_short_name(
    aggregation_strategy: Literal["majority", "worst", "best"], 
    hallucinated_classes: List[FaithBenchLabel]
    ) -> str:

    mapping_hallucinated_classes_to_short_name = {
        FaithBenchLabel.Unwanted: "U",
        FaithBenchLabel.Unwanted_Intrinsic: "UI",
        FaithBenchLabel.Unwanted_Extrinsic: "UE",
        FaithBenchLabel.Questionable: "Q",
        FaithBenchLabel.Benign: "B"
    }

    hallucinated_classes_short_names = [mapping_hallucinated_classes_to_short_name[cls] for cls in hallucinated_classes]

    if "UI" in hallucinated_classes_short_names and "UE" in hallucinated_classes_short_names:
        hallucinated_classes_short_names.remove("UI")
        hallucinated_classes_short_names.remove("UE")

    print (hallucinated_classes_short_names)

    return f"{aggregation_strategy}_{'+'.join(hallucinated_classes_short_names)}"    

# %%
def binarize_all_batches(
    aggregation_strategy: Literal["majority", "worst", "best"], 
    hallucinated_classes: List[FaithBenchLabel], 
    dump_dir: str
    ) -> List[FaithBenchTextPair]:

    binarized_samples: List[FaithBenchTextPair] = []
    for batch in tqdm(range(1, 16+1)):
        binarized_samples.extend(binarize_batch(batch_id = batch, aggregation_strategy=aggregation_strategy, hallucinated_classes=hallucinated_classes))

    config_short_name = gen_config_short_name(aggregation_strategy, hallucinated_classes)
    with open(f"{dump_dir}/faithbench_binarized_{config_short_name}.jsonl", "w") as f:
        for sample in binarized_samples:
            f.write(json.dumps(sample.model_dump()) + "\n")   

    return binarized_samples

# %%
config = {
    "aggregation_strategy": "worst",
    "hallucinated_classes": [FaithBenchLabel.Questionable, FaithBenchLabel.Unwanted, FaithBenchLabel.Unwanted_Intrinsic, FaithBenchLabel.Unwanted_Extrinsic], 
    "dump_dir": "../data_for_release"
}

_ =binarize_all_batches(**config)

# %%



