from . import params
from .. import metrics
from . import Task

audio_text_to_text = Task(
    "Audio-Text to Text",
    targets=Task.targets.text,
    metrics=[metrics.wer, metrics.cer], # TODO: blue, rouge
    parameters=params.unknown, 
    toinstance=([str], lambda x: isinstance(x, str)),
)
image_text_to_text = Task(
    "Audio-Text to Text",
    targets=Task.targets.text,
    metrics=[],                         # TODO: blue, rouge, meteor, cider, spice
    parameters=params.unknown, 
    toinstance=([str], lambda x: isinstance(x, str)),
)
visual_question_answering = Task(
    "Visual Question Answering",
    targets=Task.targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro], # TODO: Exact Match (EM), blue, meteor, VQA Accuracy
    parameters=params.classification,  
    toinstance=([str], lambda x: isinstance(x, str)),
)
document_question_answering = Task(
    "Document Question Answering",
    targets=Task.targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro], # TODO: Exact Match (EM), blue, meteor
    parameters=params.classification, 
    toinstance=([str], lambda x: isinstance(x, str)),
)
video_text_to_text = Task(
    "Video-Text to Text",
    targets=Task.targets.text,
    metrics=[],                         # TODO: blue, rouge, meteor, CIDEr, spice
    parameters=params.classification, 
    toinstance=([str], lambda x: isinstance(x, str)),
)