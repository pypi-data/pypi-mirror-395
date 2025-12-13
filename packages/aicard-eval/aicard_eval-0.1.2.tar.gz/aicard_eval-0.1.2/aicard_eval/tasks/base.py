class targets:
    text = ["solution","answer","output","response","conversations","inferences","messages","texts","caption","summary",]
    image = ["image","url"]
    video = ["video","url","video_path","video_file",]
    classes = ["label","class_name","ground_truth","emotion",]
    depth = ["depth"]
    mask = ["mask"]
    imgfeatextr = []
    keypoint = []
    featextr = []
    segmentation = {
        "target": ["seg"],
        "label": ["cat", "label"],  # candidate names for target. Must be a set of those
        "obj": ["objects"],
    }
    objdetect = {
        "target": ["box"],
        "label": ["cat", "label"],
        "obj": ["objects"],
    }

class Task:
    def __init__(self, name: str, targets:list[str], metrics: list, parameters, toinstance):
        self.name = name
        self.metrics = metrics
        self.targets = targets
        self.parameters = parameters
        self.toinstance = toinstance
    targets = targets

    def assert_output_type(self, out_sample):
        types, checker = self.toinstance  # e.g., types=[str] and checker=lambda x: isinstance(x, str)
        if checker(out_sample): return True
        raise ValueError(f'Expected one of: {", ".join(str(i) for i in types)}, but got {repr(out_sample)}')
