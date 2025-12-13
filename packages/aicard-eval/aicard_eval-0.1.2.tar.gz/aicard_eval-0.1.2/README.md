# AICard-Eval

This is a package created under the AI-CODE and it's part of the transparency services for AI model cards. Its purpose is to provide a single tool for evaluating AI models. The output is standardized and meant (but not restricted) to be used as an import for aicard package.

*Notice:*
*This is an alpha version. Some functions might not work as intended. Suported cases are text and image classifications (binary, multiclass, and multilabel),  and object detection.*

## ⚡ Quickstart

To install use:

```
conda create -n aicard-eval python=3.11
conta activate aicard-eval
pip install aicard-eval
```
or if you clone this repo
```
pip install -e .
```
Follow the script bellow. The aicard-eval will choose the correct metrics corresponding to your case. For more examples see the examples/ folder. 

You can use datasets and models from service providers e.g. huggingface or you can use your local models and datasets. Supported datasets types are: .csv, .tsv, .json, .jsonl, .xml, .yml, .yaml, .parquet, .feather, .pickle and supported image types are .jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif

```python
import aicard_eval
from datasets import load_dataset
from transformers import pipeline

# 1) Load your model
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# 2) Load your dataset
dataset = load_dataset("google-research-datasets/go_emotions", split='test')
class_names = dataset.features["labels"].feature.names


# 3) Define a function to handle the dataset
def pipeline(data):
        sentences = [text for text in data['text']]
        model_outputs = classifier(sentences)
        out = []
        for sample in model_outputs:
            flat = {d['label']: d['score'] for d in sample}
            out.append([flat[name] for name in class_names])
        return out

# 4) call the aicard-eval evaluate function
metrics = aicard_eval.evaluate(
    data=dataset,
    pipeline=pipeline,
    task=aicard_eval.tasks.nlp.text_classification,
    batch_size=32)

print(metrics)
# {'package version': '0.1.0', 
# 'datetime': '2025-Nov-14 14:54', 
# 'task': 'Text Classification', 
# 'energy consumption': 0.0006384167860318 kWh
# 'metrics': {
#     'precision_macro': 0.5090416420534856, 
#     'precision_micro': 0.5741662060070021, 
#     'recall_macro': 0.46497245851260965, 
#     'recall_micro': 0.5741662060070021, 
#     'top1_acc_micro': 0.5741662060070021, 
#     'top1_acc_macro': 0.5741662060070021, 
#     'top1_acc_weighted': 0.5741662060070021, 
#     'f1_macro': 0.4661938061623436, 
#     'f1_micro': 0.5741662060070021, 
#     'auc_roc_macro': 0.9286682043487104, 
#     'auc_roc_weighted': 0.9099991445506153}, 
# 'batch_size': 32, 
# 'hardware': 'CPU: AMD Ryzen 7 7800X3D 8-Core Processor, RAM: 15.62 GB, CUDA: | NVIDIA-SMI 580.102.01 Driver Version: 581.57  CUDA Version: 13.0|', 
# 'execution_time': 'inference: 34.68s, metrics: 45.76ms', 
# 'num_classes': 28}
```

or if you want the output in a model card format:

```
metrics = aicard_eval.evaluate(
    data=dataset,
    pipeline=pipeline,
    task=aicard_eval.tasks.nlp.text_classification,
    batch_size=32,
    as_card=True)

print(metrics)
```

## 💡 Pipeline Instructions

The pipeline funtion is the inference loop that the evaluate function calls to generate the predictions of the model. It is completely abstract which means it can contain whatever the user wants. There are only two rules to follow to construct the pipeline:

1) It must have a single function parameter `def pipeline(data)`
2) It must return a specific format depending on the task.

The package supports several formats for each task but until they are thoroughly tested here is a list you can follow:
| Task | Return Format | Example |
|----------|----------|----------|
| Binary Classification    | list [ int ] | [ 0,1,0,0 ] |
| Multi-class Classification    | list[ int ] |  [ 2,9,3,0 ] |
| Multi-label Classification    | list[ list[ int ] ] |  [ [ 2 ],[ 9,3 ],[ 3,0,1 ],[ 0 ] ] |
| Object Detection    | list[ dict ] | [{<br>"boxes": [ [ 25, 27, 37, 54 ], [ 119, 111, 40, 67 ] ],<br>"labels": [ 0, 1 ],<br>"scores": [ .88, .70 ]<br>},<br>{<br>"boxes": [ [ 64, 111, 64, 58 ] ],<br>"labels": [ 0 ],<br>"scores": [ .71 ]`<br>}] |

<br>

On the other hand `data` is basically the dataset the user imported split into batches of size `batch_size`. A loop will call the pipeline function until all batches are processed by it. The `data` is a dictionary of lists `dict[str, list]`. For example if we import a .csv:

```
name, age
Alice, 30
Bob, 25
Charlie, 35
```
with `batch_size=3` then 
```
>>> data['name']
['Alice', 'Bob', 'Charlie']
>>> data['age'][0]
30
```
