# FaithBench


Samples are in this format
```json
[
  {
    "sample_id": 0,
    "source": "Poseidon (film) . Poseidon grossed $ 181,674,817 at the worldwide box office on a budget of $ 160 million .",
    "summary": " The film \"Poseidon\" grossed $181,674,817 at the worldwide box office, with a production budget of $160 million.",
    "annotations": [
      {
        "annot_id": 1,
        "sample_id": 0,
        "annotator": "a3ac21668e6249b7978617da547f2708",
        "label": [
          "Unwanted",
          "Unwanted.Instrinsic"
        ],
        "note": "\"budget\" (source) vs. \"production budget\" (summary)\nThe budget for a movie may also include non-production budget such as distribution, advertising. ",
        "annotator_name": "XXXX",
        "summary_span": "production",
        "summary_start": 78,
        "summary_end": 88
      },
      {
        "annot_id": 60,
        "sample_id": 0,
        "annotator": "69a785fa7f454e7da5eef3c608b2133a",
        "label": [
          "Unwanted",
          "Unwanted.Instrinsic"
        ],
        "note": "\"budget\" (source) vs. \"production budget\" (summary) The budget for a movie may also include non-production budget such as distribution, advertising. ",
        "annotator_name": "XXXX",
        "summary_span": "production",
        "summary_start": 78,
        "summary_end": 88
      }
    ],
    "meta_model": "mistralai/Mistral-7B-Instruct-v0.3",
    "meta_hhemv1": 0.9995,
    "meta_hhem-2.1": 0.52694,
    "meta_hhem-2.1-english": 0.98313,
    "meta_trueteacher": 1,
    "meta_true_nli": 1,
    "meta_gpt-3.5-turbo": 1,
    "meta_gpt-4-turbo": 1,
    "meta_gpt-4o": 1,
    "meta_sample_id": 15
  },
  ...
]
```    

## License: 
CC BY-NC-SA. 

By NC, you are prohibited to use any derivation of this dataset to produce anything for commercial use, including but not limited to, finetuning commercial models using the dataset directly or indirectly. Indirect use includes but is not limited to using this dataset to augment more training data for training a model and using this dataset to train a model that infludences the training of another commercial model. 
This dataset can only be used for research purpose. 
