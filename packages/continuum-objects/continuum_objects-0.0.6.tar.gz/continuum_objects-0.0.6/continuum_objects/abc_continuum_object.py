from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from typing import Literal

ContinuumTypes = Literal[
    "SuperComputer",
    "Partition",
    "NodeGroup",
    "CPU",
    "MotherBoard",
    "GPU",
    "RAM",
    "Datacenter",
    "Throughput",
    "Network",
    "Continuum",
]


class ABCContinuumObjectNoId(BaseModel):
    type: Annotated[
        ContinuumTypes,
        Field(
            description="Type of the object, follows the exa-atow ontology",
            examples=["Cluster", "Node", "Partition"],
        ),
    ]
    name: Annotated[
        str | None,
        Field(
            default=None,
            description="Name of the object, should not be use as an identifier, prefer to use `id`",
            examples=["gpu_p13", "Jean-Zay", "compute-node", "Intel Xeon Gold 6248"],
        ),
    ]

    @property
    def summary(self) -> str:
        """
        This method should be overrided to return a text summary of the object.
        """
        return f"{self.name} - [{self.type}]"


class ABCContinuumObject(ABCContinuumObjectNoId):
    id: Annotated[
        UUID,
        Field(
            description="Unique identifier of the object accross the continuum - uuidv4",
            examples=[
                "33ced650-bcb4-4763-947b-2aa7712a61f9",
                "47fe7b4e-5c44-4c95-bde9-deb09e615cf7",
            ],
        ),
    ]

    @property
    def summary(self):
        """
        Override superclass method by adding id. Subclass should override this.
        """
        return f"{self.name} - [{self.type}] - {self.id}"
