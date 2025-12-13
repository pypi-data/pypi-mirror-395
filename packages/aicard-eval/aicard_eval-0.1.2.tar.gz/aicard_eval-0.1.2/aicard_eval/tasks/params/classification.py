import numpy as np

def main(data, preds, target_column, num_classes, anns):
    num_classes_model = num_classes
    target = []
    for batch in data:  # flatten the batch data[target_column]
        target.extend(batch[target_column])
    if isinstance(target[0], int):
        num_classes = num_classes_model if num_classes_model is not None else len(set(target))
        assert num_classes >= 2, f"found only {num_classes} classes in the dataset. Can't calculate metrics"
        class_task = "binary" if num_classes == 2 else "multiclass"
    elif isinstance(target[0], list):
        class_task = "multilabel"
        if num_classes_model is not None:
            num_classes = num_classes_model
        else:
            classes = set()
            for sample in target: classes |= set(sample)
            num_classes = len(classes)
        for t in target:  # correct the format
            if len(t) != num_classes:
                for i in range(len(target)):
                    reconstruct = [0] * num_classes
                    for cl in target[i]: reconstruct[cl] = 1
                    target[i] = reconstruct
                break
    else:
        raise AssertionError("Could not detect classification data format")
    return {
        "preds": np.array(preds),#.to(device),
        "target": np.array(target),#.to(device),
        "task": class_task,
        "num_classes": num_classes
    }