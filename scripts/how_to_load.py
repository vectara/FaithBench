import json
from typing import List, Dict

from faithbench_schema import FaithBenchBatch, FaithBenchSample, FaithBenchAnnotation, FaithBenchMetaInfo, FaithBenchLabel

FAITHBENCH_DIR = "../data_for_release"

def load_one_batch(batch_id: int) -> List[FaithBenchSample]:
    with open(f"{FAITHBENCH_DIR}/batch_{batch_id}.json", "r") as f:
        batch: FaithBenchBatch = FaithBenchBatch.model_validate_json(f.read())
        batch: Dict = batch.model_dump(by_alias=True) # this returns a dict with the field names as the keys
        batch = batch["samples"]
        batch = [FaithBenchSample.model_validate(sample) for sample in batch]
    return batch

if __name__ == "__main__":
    batch = load_one_batch(1)
    print (json.dumps(batch[:3], indent=2))

