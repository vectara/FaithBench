# %% [markdown]
# The purpose of this script is to fix a few minor clerical issues in the data before NAACL 2025. 
# It enforce the data schema and typechecking. 

# %%
import json
import tqdm

from faithbench_schema import FaithBenchSample, FaithBenchAnnotation, FaithBenchMetaInfo, FaithBenchLabel, FaithBenchBatch

# %%
# load batch_{bathc_id}_annotation.json

def load_one_batch(batch_id):
    with open(f"annot/batch_{batch_id}_annotation.json", "r") as f:
        data = json.load(f)
    return data

# %%
def convert_format(sample: dict): 
    new_annots = []
    for annot in sample["annotations"]:
        annot["annotator_id"] = annot["annotator"]
        annot.pop("sample_id") # redundant
        annot.pop("annotator") # replaced by annotator_id

        if "Unwanted.Instrinsic" in annot["label"]: # fix a typo
            annot["label"].remove("Unwanted.Instrinsic")
            annot["label"].append("Unwanted.Intrinsic")

        annot["label"] = [FaithBenchLabel(label) for label in annot["label"]]
            
        try: 
            annot = FaithBenchAnnotation(**annot)
            new_annots.append(annot)
        except Exception as e:
            print (f"Error converting annotation for sample {sample['sample_id']}: {e}")
            print (json.dumps(annot, indent=2))
            print ("+====================ONE Exception=========")
            continue 

    try: 
        metadata = FaithBenchMetaInfo(
            summarizer=sample["meta_model"],
            hhemv1=sample["meta_hhemv1"],
            hhem_2_1=sample["meta_hhem-2.1"],
            hhem_2_1_english=sample["meta_hhem-2.1-english"],
            trueteacher=sample["meta_trueteacher"],
            true_nli=sample["meta_true_nli"],
            gpt_35_turbo=sample["meta_gpt-3.5-turbo"],
            gpt_4_turbo=sample["meta_gpt-4-turbo"],
            gpt_4o=sample["meta_gpt-4o"],
            raw_sample_id=sample["meta_sample_id"],
        )
    except Exception as e:
        print (f"Error converting metadata for sample {sample['sample_id']}: {e}")
        print (json.dumps(sample, indent=2))
        exit()

    return FaithBenchSample(# re-instantiate the sample
        sample_id=sample["sample_id"],
        source=sample["source"],
        summary=sample["summary"],
        annotations=new_annots, # just updated above 
        metadata=metadata,
    )

def convert_batch(batch_id, dump_dir = "data_for_release"): 
    batch_data = load_one_batch(batch_id)
    new_batch_data = []
    for sample in batch_data:
        new_sample = convert_format(sample)
        if new_sample is not None:
            new_batch_data.append(new_sample)

    new_batch = FaithBenchBatch(samples=new_batch_data)

    # dump the converted data
    with open(f"{dump_dir}/batch_{batch_id}.json", "w") as f:
        json.dump(new_batch.model_dump(by_alias=True), f, indent=2)
    return batch_data

# %%
for i in tqdm.tqdm(range(1, 16+1)):
    print (f"Converting batch {i}")
    if i == 13:
        continue
    else: 
        _ = convert_batch(i)


