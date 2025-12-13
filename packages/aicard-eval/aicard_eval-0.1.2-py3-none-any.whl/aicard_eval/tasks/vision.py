import numpy as np
from typing import Tuple
from . import params
from .. import metrics
from . import Task

depth_estimation = Task(
    "Depth Estimation",
    targets=Task.targets.depth,
    metrics=[metrics.mae, metrics.rmse, metrics.ssim, metrics],  # TODO: sirmse (Scale-Invariant rmse)
    parameters=params.classification, 
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_segmentation = Task(
    "Image Segmentation",
    targets=Task.targets.segmentation, # special value
    metrics=[metrics.iou,metrics.dice_macro, metrics.dice_micro], # TODO: pixel acc, metrics.map
    parameters=params.unknown,
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

object_detection = Task(
    "Object Detection",
    targets=Task.targets.objdetect, # special value
    metrics=[metrics.od_metrics],
    parameters=params.object_detection,
    toinstance=(
            [dict[str, list], Tuple[list[list[int]], list[int], list[float]], list[int], list[float]],
            lambda x: (
                isinstance(x, list)
                and len(x) == 3
                and isinstance(x[0], list)
                and all(
                    isinstance(sublist, list)
                    and len(sublist) == 4
                    and all(isinstance(i, int) for i in sublist)
                    for sublist in x[0]
                )
                and isinstance(x[1], list)
                and all(isinstance(i, int) for i in x[1])
                and isinstance(x[2], list)
                and all(isinstance(f, float) for f in x[2])
            ) # box, cat_id, score,
            or (
                isinstance(x, dict)
                and len(x)==3
                and "scores" in x
                and isinstance(x["scores"], list)
                and "labels" in x
                and isinstance(x["labels"], list)
                and "boxes" in x
                and isinstance(x["boxes"], list)
            ),
        ),
)

image_classification = Task(
    "Image Classification",
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

text_to_image = Task(
    "Text to Image",
    targets=Task.targets.image,
    metrics=[metrics.ssim], # TODO: Inception Score (IS), Fréchet Inception Distance (fid), CLIPScore
    parameters=params.unknown,
    toinstance= ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_to_text = Task(
    "Image to Text",
    targets=Task.targets.text,
    metrics=[],  # TODO: blue, rouge, meteor, CIDEr, spice
    parameters=params.classification, 
    toinstance=([str], lambda x: isinstance(x, str)),
)

image_to_image = Task(
    "Image to Image",
    targets=Task.targets.image,
    metrics=[metrics.ssim, metrics.psnr],  # TODO: lpips (Perceptual Loss)
    parameters=params.unknown, 
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray))
)

image_to_video = Task(
    "Image to Video",
    targets=Task.targets.video,
    metrics=[metrics.ssim, metrics.psnr],  # TODO: FVD (Fréchet Video Distance)
    parameters=params.unknown,
    toinstance=(list[np.ndarray],lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),),
)

video_classification = Task(
    "Video Classification",
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

text_to_video = Task(
    "Text to Video",
    targets=Task.targets.video,
    metrics=[metrics.ssim],     # TODO: FVD, IS, Fid
    parameters=params.unknown,
    toinstance=(list[np.ndarray],lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),),
)

mask_generation = Task(
    "Text to Video",
    targets=Task.targets.mask,
    metrics=[metrics.iou, metrics.dice_macro, metrics.dice_micro], # TODO: Pixel Accuracy
    parameters=params.unknown, 
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_feature_extraction = Task(
    "Image Feature Extraction",
    targets=Task.targets.imgfeatextr,
    metrics=[], # TODO: Cosine Similarity,Euclidean Distance,lpips
    parameters=params.unknown, 
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

keypoint_detection = Task(
    "Keypoint Detection",
    targets=Task.targets.keypoint,
    metrics=[metrics.rmse],     # TODO: Percentage of Correct Keypoints (PCK), Normalized Mean Error (NME), Mean Squared Error (MSE)
    parameters=params.unknown, 
    toinstance=(
        list[Tuple[int, int]],
        lambda x: isinstance(x, list)
        and all(
            isinstance(t, tuple)
            and len(t) == 2
            and isinstance(t[0], int)
            and isinstance(t[1], int)
            for t in x
        ),
    ),
)

