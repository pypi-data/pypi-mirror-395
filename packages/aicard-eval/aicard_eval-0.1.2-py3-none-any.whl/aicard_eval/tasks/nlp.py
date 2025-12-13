import numpy as np
from . import params
from .. import metrics
from . import Task

question_answering = Task(
    "Question Answering",
    targets=Task.targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro],  # TODO: Exact Match (EM)
    parameters=params.unknown,
    toinstance=([str], lambda x: isinstance(x, str)),
)

translation = Task(
    "Translation",
    targets=Task.targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, chrF++
    parameters=params.unknown, 
    toinstance=([str], lambda x: isinstance(x, str)),
)

summarization = Task(
    "Summarization",
    targets=Task.targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore
    parameters=params.unknown,
    toinstance=([str], lambda x: isinstance(x, str)),
)

feature_extraction = Task(
    "Translation",
    targets=Task.targets.featextr,
    metrics=[],  # TODO: Cosine Similarity,Euclidean Distance,Pearson Correlation
    parameters=params.unknown,
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

text_generation = Task(
    "Text Generation",
    targets=Task.targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore, Perplexity
    parameters=params.unknown,
    toinstance=([str], lambda x: isinstance(x, str)),
)

text_to_text_generation = Task(
    "Text to Text Generation",
    targets=Task.targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore, chrF++"
    parameters=params.unknown,
    toinstance=([str], lambda x: isinstance(x, str)),
)

text_classification = Task(
    "Text Classification",
    targets=Task.targets.classes,
    metrics=[metrics.precision_macro, metrics.precision_micro,
             metrics.recall_macro, metrics.recall_micro,
             metrics.top1_acc_micro, metrics.top1_acc_macro, metrics.top1_acc_weighted,
             metrics.f1_macro, metrics.f1_micro,
             metrics.auc_roc_macro, metrics.auc_roc_weighted],
    parameters=params.classification,
    toinstance=(
        [np.ndarray, int, float, list[float], str, dict[str, float]],
        lambda x: (
            isinstance(x, (np.ndarray, int, float, str))
            or (isinstance(x, list) and all(isinstance(i, float) for i in x))
            or (
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, float)
                    for k, v in x.items()
                )
            )
        ),
    ),
)