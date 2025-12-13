import platform, subprocess, psutil
import os
import csv
import sys
import yaml
import datasets
import pandas as pd
from . import tasks


def human_readable_time(seconds: float) -> str:
    if seconds < 1e-3:  # less than 1 millisecond
        return f"{seconds * 1e6:.2f}µs"
    elif seconds < 1:  # less than 1 second
        return f"{seconds * 1e3:.2f}ms"
    elif seconds < 60:  # less than 1 minute
        return f"{seconds:.2f}s"
    elif seconds < 3600:  # less than 1 hour
        minutes = int(seconds // 60)
        sec = seconds % 60
        return f"{minutes}min {sec:.2f}s"
    else:  # 1 hour or more
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        sec = seconds % 60
        return f"{hours}h {minutes}min {sec:.2f}s"

def get_hardware_info(emission):
    # cpu_info = "Not found"
    # try:
    #     with open("/proc/cpuinfo") as f:
    #         for line in f:
    #             if "model name" in line:
    #                 cpu_info = line.strip().split(":")[1].strip()
    # except FileNotFoundError:
    #     cpu_info = platform.processor() or platform.machine()

    ram_bytes = psutil.virtual_memory().total
    ram_gb = round(ram_bytes / (1024 ** 3), 2)
    cuda_version = "Not found"
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "CUDA Version" in line:
                    cuda_version = line.strip()
                    break
    except FileNotFoundError:
        pass
    if cuda_version == "Not found":
        try:
            result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "release" in line:
                        cuda_version = line.strip()
                        break
        except FileNotFoundError:
            pass

    return f"CPU: {emission['CPU_name']}, RAM: {ram_gb} GB, GPU: {emission['GPU_name']} CUDA: {cuda_version}"


def is_path(s):
    return isinstance(s, str) and os.path.exists(os.path.expanduser(s))

def get_supported_types():
    return [".csv",".tsv",".json",".jsonl",".xml",".yml",".yaml",".parquet",".feather",".pickle"".html"]

def get_supported_image_types():
    return [".jpg",".jpeg",".png",".gif",".bmp",".tiff",".tif"]

def determine_type(path):
    _, extension = os.path.splitext(path)
    return extension

def read_pd(path, delimiter=None, names=None, split=None):
    # TODO: split is unused
    supported_types = get_supported_types()
    t = determine_type(path)
    if t == supported_types[0]:  # .csv
        csv.field_size_limit(sys.maxsize)
        return (
            pd.read_csv(path, names=names, engine="python")
            if delimiter is None
            else pd.read_csv(path, delimiter=delimiter, names=names, engine="python")
        )
    if t == supported_types[1]:  # .tsb
        csv.field_size_limit(sys.maxsize)
        return pd.read_csv(path, delimiter=delimiter, names=names, engine="python")
    if t == supported_types[2]: return pd.read_json(path)
    if t == supported_types[3]: return pd.read_json(path, lines=True)
    if t == supported_types[4]: return pd.read_xml(path)
    if t == supported_types[5] or t == supported_types[6]:  # .yml .yaml
        with open(path, "r") as file:
            yaml_data = yaml.safe_load(file)
        return pd.DataFrame(yaml_data)
    if t == supported_types[7]: return pd.read_parquet(path)
    if t == supported_types[8]: return pd.read_feather(path)
    if t == supported_types[9]: return pd.read_pickle(path)
    if t == supported_types[10]:  return pd.read_html(path)[0]
    raise AssertionError(f"read_data_structure: Type of {t} is not one of: {', '.join(get_supported_types())}")

def read_data(path, delimiter=None, names=None, split=None):
    return datasets.Dataset.from_pandas(read_pd(path, delimiter=delimiter, names=names, split=split))

class BoxFormatHelpers:
    @staticmethod
    def xyxy2xywh(xyxy):
        x_min, y_min, x_max, y_max = xyxy
        w = x_max - x_min
        h = y_max - y_min
        return x_min, y_min, w, h

    @staticmethod
    def xywh2xyxy(xywh):
        x_min, y_min, w, h = xywh
        x_max = x_min + w
        y_max = y_min + h
        return x_min, y_min, x_max, y_max

    @staticmethod
    def determine_xyxy_or_xywh(bbox, img_w, img_h):
        x_min, y_min, curious1, curious2 = BoxFormatHelpers.xyxy2xywh(bbox)
        if curious1 < 0 or curious2 < 0:
            return "xywh"
        x_min, y_min, curious1, curious2 = BoxFormatHelpers.xywh2xyxy(bbox)
        if curious1 > img_w or curious2 > img_h:
            return "xyxy"
        # warnings.warn("Warning: Can't determine bbox format. Assuming xyxy. Consider using the box_format option")
        return None


def convert_to_datasets(data):
    if isinstance(data, datasets.Dataset): return data
    if isinstance(data, dict): return datasets.Dataset.from_dict(data)
    if isinstance(data, list): return datasets.Dataset.from_list(data)
    raise AssertionError(f"Dataset of type {type(data)} is not supported")

def anns_to_datasets(anns):
    # assuming anns is a list
    if isinstance(anns[0], dict): return datasets.Dataset.from_list(anns)
    anns = [datasets.Dataset.from_list(ann) for ann in anns]
    anns = [datasets.Dataset.to_dict(ann) for ann in anns]
    return datasets.Dataset.from_list(anns)


def check_validity_of_target(data, task: tasks.Task, target_column: str|None=None):
    if task==tasks.vision.image_segmentation or task == tasks.vision.object_detection:
        target_column = handle_object_special_case(data, task)
        return target_column
    if target_column is not None:
        for key in data:
            if target_column in key:
                return target_column
    t2t = task.targets
    targets_found = []
    for candidate in t2t:
        for key in data:
            if candidate.lower() in key.lower():  # cases insensitive match
                targets_found.append(key)
    assert len(targets_found), f"""Expected one of {', '.join('"'+i+'"' for i in t2t)}, but got {', '.join('"'+key+'"' for key in data)}"""
    assert len(targets_found) == 1, f"""Found more that one match to target: {', '.join('"'+i+'"' for i in targets_found)}. Use the option "target" to choose which one you want"""
    return targets_found[0]



def handle_object_special_case(data, task: tasks.Task):
    t2t = task.targets
    targets_found = []
    for candidate_object in t2t["obj"]:
        for key in data:
            if candidate_object.lower() in key.lower():  # we have an object
                if isinstance(data[key], dict):
                    for candidate_target in t2t["target"]:
                        t = []
                        t_found = 0
                        l_found = 0
                        for k in data[key]:
                            if candidate_target.lower() in k.lower():
                                t.append(k)
                                t_found += 1
                            for candidate_label in t2t["label"]:
                                if candidate_label.lower() in k.lower():
                                    t.append(k)
                                    l_found += 1
                        if t_found == 1 and l_found == 1:
                            return [key, t[0], t[1]]  # object, target, label
                elif isinstance(data[key], list):
                    for candidate_target in t2t["target"]:
                        t = []
                        t_found = 0
                        l_found = 0
                        for k in data[key][0]:
                            if candidate_target.lower() in k.lower():
                                t.append(k)
                                t_found += 1
                            for candidate_label in t2t["label"]:
                                if candidate_label.lower() in k.lower():
                                    t.append(k)
                                    l_found += 1
                        if t_found == 1 and l_found == 1:
                            return [key, t[0], t[1]]  # object, target, label
    # if we don't have an object
    for candidate_target in t2t["target"]:
        t = []
        t_found = 0
        l_found = 0
        for k in data:
            if candidate_target.lower() in k.lower():
                t.append(k)
                t_found += 1
            for candidate_label in t2t["label"]:
                if candidate_label.lower() in k.lower():
                    t.append(k)
                    l_found += 1
        if t_found == 1 and l_found == 1:
            return [t[0], t[1]]  # target, category

