import json
import requests
from .abc_continuum_object import ABCContinuumObject
from .clusters import SuperComputer, Partition, NodeGroup, CPU, MotherBoard, GPU, RAM
from .data_centers import DataCenter
from .network import Network
from .continuum import Continuum

constructors: dict[str, type] = {
    "SuperComputer": SuperComputer,
    "Partition": Partition,
    "NodeGroup": NodeGroup,
    "CPU": CPU,
    "MotherBoard": MotherBoard,
    "GPU": GPU,
    "RAM": RAM,
    "Datacenter": DataCenter,
    "Network": Network,
    "Continuum": Continuum,
}


def from_json(path_or_url: str) -> ABCContinuumObject:
    if path_or_url[:4] == "http":
        d = from_json_url(url=path_or_url)
    else:
        d = from_json_path(path=path_or_url)

    continuum_type = d["type"]
    if continuum_type not in constructors:
        raise ValueError(
            f"Value {continuum_type} not known for continuum objects. Known types are : {constructors.keys()}."
        )

    const = constructors[continuum_type]
    result = const.model_validate(d)
    return result


def from_json_path(path: str) -> dict:
    with open(path, "rt") as f:
        d = json.load(f)
    return d


def from_json_url(url: str) -> dict:
    req_res = requests.get(url)
    if req_res.status_code != 200:
        raise requests.HTTPError(f"could not retrieve date from url {url}")
    content = req_res.content
    d = json.loads(content)
    if "type" not in d:
        raise KeyError("Key 'type' must be at the root of the downloaded json")

    return d
