from .abc_continuum_object import ABCContinuumObject
from .generic_objects import MeasuredValue
from .clusters import SuperComputer
from .data_centers import DataCenter
from uuid import UUID
from typing import Annotated
from pydantic import Field, BaseModel


class NetworkEdge(BaseModel):  # TODO: add validation of start and end as node labels
    start: Annotated[
        str, Field(description="Label of the node from which the edge starts")
    ]
    end: Annotated[
        str, Field(description="Label of the node towards which the edge stops")
    ]
    throughput: Annotated[
        MeasuredValue, Field(description="Measured value of the throughput")
    ]


class NetworkNode(BaseModel):
    id: Annotated[
        UUID,
        Field(
            description="Unique identifier for the graph node. Valid only in the perimeter of the graph"
        ),
    ]
    continuum_object_id: Annotated[
        UUID,
        Field(
            description="ID in the Continuum Digital Twin of the object represented by the node"
        ),
    ]
    label: Annotated[str, Field("Label used to identify the node")]


class Network(ABCContinuumObject):
    nodes: Annotated[
        list[NetworkNode], Field(description="List of nodes on the network graph")
    ]
    edges: Annotated[
        list[NetworkEdge], Field(description="Description of the edges on the network")
    ]

    def get_throughput(self, start_label: str, end_label: str) -> MeasuredValue | None:
        for each_edge in self.edges:
            if each_edge.start == start_label and each_edge.end == end_label:
                return each_edge.throughput
