from datetime import datetime
import time
import inspect
import pickle
from .emissions import Emission
from .card.model_card import ModelCard

import aicard_eval
from .utils import (human_readable_time,
                              get_hardware_info,
                              is_path,
                              read_data,
                              convert_to_datasets,
                              anns_to_datasets,
                              check_validity_of_target)


def autocall(metric, **kwargs):
    args = set(inspect.signature(metric).parameters.keys())
    kwargs = {k: v for k, v in kwargs.items() if k in args}
    try: return metric(**kwargs)
    except TypeError as e:
        print(e)
        return None
    
def pipeline_loop(data, pipeline, cache_path):
    if cache_path:
        print(f"Loading cache from {cache_path}")
        with open(cache_path, "rb") as f:
            cache = pickle.load(f)
        return cache["preds"], cache["execution_time"]

    preds = []
    start = time.time()
    for batch in data:
        preds.extend(pipeline(batch))
    pipe_execution_time = time.time() - start

    with open('cache.pkl', "wb") as f:
        pickle.dump({
            "preds": preds,
            "execution_time": pipe_execution_time
        }, f)

    return preds, pipe_execution_time

def evaluate_to_card(info: dict) -> ModelCard:
    card = ModelCard()
    card.title = f"{info['task']} Results"
    card.performance.analysis = f"Evaluation was conducted at {info['datetime']} for {info['task'].lower()} with {info['batch_size']} batch size. The source file is:<br>{info['code']}"
    card.performance.metrics = (
            f"The following metrics were computed at {info['datetime']}:<br>"
            + "".join([f"- {k}: {v}<br>" for k, v in info['metrics'].items()])
    )
    card.performance.thresholds = f"No thresholds have been applied on metric values computed at {info['datetime']}."
    card.considerations.software = f"The evaluation was conducted with <a href=\"https://pypi.org/project/aicard-eval/\">aicard_eval</a>-{info['package_version']}"
    card.considerations.hardware = "The following hardware suffices for model running and evaluation:<br>"+info['hardware']+"<br>"    
    return card

def evaluate(
    data: "path or data",
    pipeline: callable,
    task: aicard_eval.tasks.Task,
    cache_path: str = None,
    target_column:str|None=None,
    num_classes:int|None=None,  # in case the preds have more classes than target
    batch_size:int=1,
    anns: list[list[dict]]|list[dict]|None=None,
    box_format = None,
    as_card = False
) -> dict | ModelCard:
    if anns is None:
        anns = [None]
    if is_path(data):
        data = read_data(data)
    data = convert_to_datasets(data)
    data = data.batch(batch_size)
    anns = anns_to_datasets(anns)
    anns = anns.batch(batch_size)

    target_column = check_validity_of_target(anns[0] if len(anns.features) else data[0], task, target_column)
    out_sample = pipeline(data[0])
    task.assert_output_type(out_sample[0])
    
    emissions = Emission()
    emissions.start()
    preds, pipe_execution_time = pipeline_loop(data, pipeline, cache_path)
    emissions.stop()
    emission = emissions.pop()
    
    kwargs = task.parameters(
        data=data,
        preds=preds,
        target_column=target_column,
        num_classes=num_classes,
        anns=anns,
    )
    if box_format:
        kwargs['box_format'] = box_format

    if 'num_classes' in kwargs and kwargs['num_classes'] == 2: task.metrics.append(aicard_eval.metrics.precision_recall_curve)
    start = time.time()
    metrics = {metric.__name__: autocall(metric, **kwargs) for metric in task.metrics}
    metrics_execution_time = time.time() - start

    caller_path = inspect.stack()[1].filename
    with open(caller_path, 'r') as f:
        caller_content = f.read()

    out = {
        'package_version': aicard_eval.__version__,
        'datetime': datetime.now().strftime('%Y-%b-%d %H:%M'),
        'task':task.name ,
        'metrics': metrics,
        'batch_size': batch_size,
        'code': caller_content,
        'hardware': get_hardware_info(emission),
        'execution_time': f'inference: {human_readable_time(pipe_execution_time)}, metrics: {human_readable_time(metrics_execution_time)}',
        'energy_consumption': f"{emission['power_consumption(kWh)'][0]} kWh, ",
        }

    if 'num_classes' in kwargs and kwargs['num_classes']: out['num_classes'] = kwargs['num_classes']

    if as_card:
        return evaluate_to_card(out)
    
    return out
    
