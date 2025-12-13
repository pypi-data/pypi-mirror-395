from PIL import Image
import numpy as np
import warnings
from io import BytesIO
import requests

import validators

from ... import utils

def main(data, preds, target_column, num_classes, anns):
    anns_source = data if len(anns.features) == 0 else anns
    if len(target_column) == 2:
        bbox_column, label_column = target_column
        obj_column = None
    else:
        obj_column, bbox_column, label_column = target_column
    iou_type = "bbox"

    img_column, src_type = determine_img_column_src_type(data)
    # box_format = determine_box_format(data, anns_source, img_column, src_type, bbox_column)

    preds_ready = prepare_preds(preds)
    target_ready = prepare_target(anns_source, target_column, label_column, obj_column, bbox_column)

    return {
        "preds": np.array(preds_ready),
        "target": np.array(target_ready),
        "iou_type": iou_type,
        # "box_format": box_format,
        "task": "MULTILABEL",
        "num_classes": num_classes
    }

def determine_img_column_src_type(data):
    img_column = None
    src_type = None
    for key in data.column_names:  # search for the images as path or web
        if utils.is_path(data[key][0][0]):
            if utils.determine_type(data[key][0][0]) in utils.get_supported_image_types():
                img_column = key
                src_type = "path"
        elif validators.url(data[key][0][0]):
            image_formats = ["image/" + t.replace(".", "") for t in utils.get_supported_image_types()]
            r = requests.head(data[key][0][0])
            if r.headers["content-type"] in image_formats:
                img_column = key
                src_type = "url"
    return img_column, src_type

def determine_box_format(data, anns_source, img_column, src_type, bbox_column):
    box_format = None
    if src_type == "path":  # we can found the images
        for batch in data:
            for img, bboxes in zip(batch[img_column], batch[bbox_column]):
                image = Image.open(img)
                width, height = image.size
                for bbox in bboxes:
                    box_format = utils.BoxFormatHelpers.determine_xyxy_or_xywh(bbox, width, height)
                    if box_format is not None:
                        break
                if box_format is not None:
                    break
            if box_format is not None:
                break
    elif src_type == "url":
        for batch in zip(data, anns_source):
            for img, bboxes in zip(batch[0][img_column], batch[1][bbox_column]):
                image = Image.open(BytesIO(requests.get(img).content))
                width, height = image.size
                for bbox in bboxes:
                    box_format = utils.BoxFormatHelpers.determine_xyxy_or_xywh(bbox, width, height)
                    if box_format is not None:
                        break
                if box_format is not None:
                    break
            if box_format is not None:
                break
    if box_format is None:
        warnings.warn("Warning: can't determine box_format. Setting box_format = 'xyxy'. Consider using the box_format option")
        box_format = "xyxy"
    return box_format

def prepare_preds(preds):
    preds_ready = []
    if not isinstance(preds[0], dict):
        for pred in preds:
            boxes, cat_ids, scores = pred
            preds_ready.append({
                "boxes": np.array(boxes),
                "labels": np.array(cat_ids),
                "scores": np.array(scores),
            })
    else:
        preds_ready = preds
    return preds_ready

def prepare_target(anns_source, target_column, label_column, obj_column, bbox_column):
    target_ready = []
    if len(target_column) == 2:
        # bbox, label = target
        # assuming batch[bbox_column] and batch[label_column] are list or tuple
        for batch in anns_source:
            for boxes_target, cat_ids_target in zip(batch[bbox_column], batch[label_column]):
                if (boxes_target is not None) and (cat_ids_target is not None):  # prevent reading None values that the convertion to datasets creates
                    target_ready.append({
                        "boxes": np.array(boxes_target),
                        "labels": np.array(cat_ids_target),
                    })
    else:
        # obj, bbox, label = target
        if isinstance(anns_source[0][obj_column], dict):
            for batch in anns_source:
                for boxes_target, cat_ids_target in zip(
                    batch[obj_column][bbox_column], batch[obj_column][label_column]
                ):
                    if (boxes_target is not None) and (
                        cat_ids_target is not None
                    ):  # prevent reading None values that the convertion to datasets creates
                        target_ready.append({
                            "boxes": np.array(boxes_target),
                            "labels": np.array(cat_ids_target)
                        })
        else:  # elif isinstance(data[obj], list)
            for batch in anns_source:
                for object in batch[obj_column]:
                    if (object[bbox_column] is not None) and (
                        object[label_column] is not None
                    ):  # prevent reading None values that the convertion to datasets creates
                        target_ready.append({
                            "boxes": np.array(object[bbox_column]),
                            "labels": np.array(object[label_column]),
                        })
    return target_ready