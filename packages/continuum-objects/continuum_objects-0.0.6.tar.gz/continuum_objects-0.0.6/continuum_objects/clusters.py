from .abc_continuum_object import ABCContinuumObject, ABCContinuumObjectNoId
from uuid import UUID
from typing import Annotated
from pydantic import Field, NonNegativeInt, BaseModel
from .generic_objects import MeasuredValue


class ABCNodeComponents(ABCContinuumObjectNoId):
    count: Annotated[
        NonNegativeInt,
        Field(default=0, description="Number of such component on the node"),
    ]


class MotherBoard(ABCNodeComponents): ...


class RAM(ABCNodeComponents):
    capacity: Annotated[MeasuredValue, Field(description="RAM capacity, in GB")]


class CPU(ABCNodeComponents): ...


class GPU(ABCNodeComponents): ...


class NodeGroup(ABCContinuumObjectNoId):
    count: Annotated[
        NonNegativeInt,
        Field(
            default=0, description="Number of such nodes on the node group (partition)"
        ),
    ]
    nodeComponents: Annotated[
        list[ABCNodeComponents],
        Field(
            description="List of components on the node",
        ),
    ]

    @property
    def summary(self) -> str:
        result = f"Number of nodes on this group : {self.count}"
        return result


class Partition(ABCContinuumObject):
    totalNodeCount: Annotated[
        NonNegativeInt,
        Field(
            description="Total number of nodes on the partition", examples=[17, 0, 1]
        ),
    ]
    nodeGroups: Annotated[
        list[NodeGroup],
        Field(
            description="List of nodes groups on this partition. A node group is a family of identical nodes.",
        ),
    ]

    @property
    def summary(self) -> str:
        node_detail = ""
        for each_node_group in self.nodeGroups:
            node_detail += f"{each_node_group.count} `{each_node_group.name}`, "
        node_detail = node_detail[:-2]
        return f"[{self.name}] total node count: {self.totalNodeCount} ({node_detail})"


class SuperComputer(ABCContinuumObject):
    hasPartitions: Annotated[
        list[Partition],
        Field(
            description="List of partitions on the cluster",
        ),
    ]

    @property
    def summary(self) -> str:
        """
        Returns a summary of the cluster
        """
        result = (
            f"SuperComputer {self.name}, with {len(self.hasPartitions)} partitions :\n"
        )
        for each_partition in self.hasPartitions:
            result += f"    - {each_partition.summary}\n"
        return result

    @property
    def partition_names(self) -> list[str]:
        result = []
        for each_partition in self.hasPartitions:
            if each_partition.name is not None:
                result.append(each_partition.name)
        return result

    def get_partition_with_name(self, partition_name: str) -> Partition:
        """
        Returns a partition with from its name. Raises exception if no
        match is found.

        Parameters :
        ---
        - partition_name : the name of the partition

        Returns :
        ---
        The Partition object
        """
        for each_partition in self.hasPartitions:
            if each_partition.name == partition_name:
                return each_partition
        raise ValueError(
            f"No match was found with name {partition_name} among partitions. Available partition names : {self.partition_names}"
        )
