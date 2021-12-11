import struct

import numpy as np


def float_to_bin(num: float) -> str:
    binary = format(struct.unpack("!I", struct.pack("!f", num))[0], "032b")
    return binary


def bin_to_float(binary: str) -> float:
    return round(struct.unpack("!f", struct.pack("!I", int(binary, 2)))[0], 2)


class Gene(object):
    def __init__(
        self,
        gene_type: str,
        mean: float = 1.0,
        std: float = 0.5,
        min_value: float = 0.5,
        max_value: float = 1.5,
    ):
        self.gene_type = gene_type
        self.float_value = bin_to_float(
            float_to_bin(self.get_random_gene_value(mean, std, min_value, max_value))
        )
        self.binary_value = float_to_bin(self.float_value)

    def get_bit_str(self) -> str:
        return self.binary_value

    def __str__(self) -> str:
        return f"{self.gene_type} - float: {self.float_value} - binary: {self.get_bit_str()}"

    def __mul__(self, other: float) -> float:
        return self.float_value * other

    @staticmethod
    def get_random_gene_value(
        mean: float, std: float, min_value: float = 0.5, max_value: float = 1.5
    ):
        value = float(np.random.normal(mean, std))
        if value < min_value:
            value = min_value
        if value > max_value:
            value = max_value
        return round(value, 2)


class Genes(object):
    def __init__(self):
        self.speed = Gene("speed", mean=1.0, std=1.0, min_value=0.5, max_value=1.5)
        self.vision_radius = Gene(
            "vision_radius", mean=1.0, std=0.5, min_value=0.25, max_value=2.0
        )
        self.eating_penalty = Gene(
            "eating_penalty", mean=1.0, std=1.0, min_value=0.5, max_value=2.0
        )
        self.health = Gene("health", mean=1.0, std=0.5, min_value=0.25, max_value=2.0)
        self.hunger = Gene("hunger", mean=1.0, std=0.5, min_value=0.25, max_value=2.0)
        self.lifespan = Gene(
            "lifespan", mean=1.0, std=0.5, min_value=0.25, max_value=2.0
        )
        self.reproduce_cycle = Gene(
            "reproduce_cycle", mean=1.0, std=1.0, min_value=0.5, max_value=2.0
        )

    def get_bit_str(self) -> str:
        return (
            self.speed.get_bit_str()
            + self.vision_radius.get_bit_str()
            + self.eating_penalty.get_bit_str()
            + self.health.get_bit_str()
            + self.hunger.get_bit_str()
            + self.lifespan.get_bit_str()
            + self.reproduce_cycle.get_bit_str()
        )

    def get_bit_array(self):
        # TODO - implement getting bit array from the bit string
        return

    def __str__(self) -> str:
        return self.get_bit_str()

    @staticmethod
    def combined_genes(parent_genes_1, parent_genes_2):
        new_genes = 1
