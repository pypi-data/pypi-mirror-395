from .abc_continuum_object import ABCContinuumObject
from .clusters import SuperComputer
from .data_centers import DataCenter
from .network import Network

from uuid import UUID, uuid4


class Continuum(ABCContinuumObject):
    superComputers: list[SuperComputer]
    dataCenters: list[DataCenter]
    network: Network

    @property
    def summary(self) -> str:
        result = "Continuum made of :\n"
        result += f"    • {len(self.superComputers)} cluster{'' if len(self.superComputers) <= 1 else 's'} :\n"
        for each_hpc in self.superComputers:
            result += f"        • {each_hpc.summary}\n"
            result += "\n"

        result += f"    • {len(self.dataCenters)} dataCenters :\n"
        for each_datacenter in self.dataCenters:
            result += f"        • {each_datacenter.summary}\n"

        result += f"    • with network graph : {self.network.summary}"

        return result

    def get_element_with_id(self, uid: str | UUID):
        all_infras = self.superComputers + self.dataCenters + [self.network]
        if not isinstance(uid, UUID):
            uid = UUID(uid)

        for each_infra in all_infras:
            if each_infra.id == uid:
                return each_infra
        raise KeyError(f"Could not find any element of Continuum with id {uid}")

    def get_element_with_name(self, name: str):
        all_infras = self.superComputers + self.dataCenters + [self.network]

        for each_infra in all_infras:
            if each_infra.name == name:
                return each_infra
        raise KeyError(f"Could not find any element of Continuum with name {name}")
