import random
import struct
from typing import Tuple, Optional, Union, Dict

import cupy as cp


def float_to_bin(num: float) -> str:
    binary = format(struct.unpack("!I", struct.pack("!f", num))[0], "032b")
    return binary


def bin_to_float(binary: str) -> float:
    return round(struct.unpack("!f", struct.pack("!I", int(binary, 2)))[0], 2)


class Gene(object):
    def __init__(
        self,
        gene_type: str,
        value: Union[Optional[float], Optional[str]] = None,
        mean: float = 1.0,
        std: float = 0.5,
        min_value: float = 0.5,
        max_value: float = 1.5,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.gene_type = gene_type
        if value is None:
            self.float_value = bin_to_float(
                float_to_bin(
                    self.get_random_gene_value(mean, std, min_value, max_value)
                )
            )
            self.binary_value = float_to_bin(self.float_value)
        elif isinstance(value, float):
            value = min(max(value, min_value), max_value)
            self.float_value = value
            self.binary_value = float_to_bin(self.float_value)
        elif isinstance(value, str):
            self.binary_value = value
            self.float_value = bin_to_float(self.binary_value)

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
        value = float(cp.random.normal(mean, std))
        if value < min_value:
            value = min_value
        if value > max_value:
            value = max_value
        return round(value, 2)

    def mutate(self, binary=False):
        if binary:
            self.mutate_binary()
        else:
            self.mutate_float()

    def mutate_float(self):
        """
        Mutate the gene by randomly changing the value
        :return:
        """
        mutation_value = cp.random.normal(-0.01, 0.05)
        self.float_value += mutation_value
        self.float_value = min(max(self.float_value, self.min_value), self.max_value)
        self.binary_value = float_to_bin(self.float_value)

    def mutate_binary(self):
        """
        Mutate the gene by randomly flipping a bit
        :return:
        """
        start_bit_string = self.binary_value[:8]
        mutable_bit_string = self.binary_value[8:16]
        end_bit_string = self.binary_value[16:]
        mutable_bits = [int(bit) for bit in mutable_bit_string]
        for i in range(len(mutable_bits)):
            if random.random() < 1 / (len(mutable_bits) ** 2):
                mutable_bits[i] = 1 - mutable_bits[i]
        mutable_bit_string = "".join(str(bit) for bit in mutable_bits)
        self.binary_value = start_bit_string + mutable_bit_string + end_bit_string
        self.float_value = min(
            max(bin_to_float(self.binary_value), self.min_value), self.max_value
        )


class Genes(object):
    def __init__(self, genes: Optional[Dict[str, Gene]] = None):
        self.number_of_genes = 7
        self.gene_length = 32
        if genes is None:
            self.speed = Gene("speed", mean=1.0, std=0.2, min_value=0.5, max_value=1.5)
            self.vision_radius = Gene(
                "vision_radius", mean=1.0, std=0.1, min_value=0.25, max_value=2.0
            )
            self.eating_penalty = Gene(
                "eating_penalty", mean=1.0, std=0.1, min_value=0.5, max_value=2.0
            )
            self.health = Gene(
                "health", mean=1.0, std=0.1, min_value=0.25, max_value=2.0
            )
            self.hunger = Gene(
                "hunger", mean=1.0, std=0.1, min_value=0.25, max_value=2.0
            )
            self.lifespan = Gene(
                "lifespan", mean=1.0, std=0.1, min_value=0.25, max_value=2.0
            )
            self.reproduce_cycle = Gene(
                "reproduce_cycle", mean=1.0, std=0.2, min_value=0.5, max_value=2.0
            )
        else:
            self.speed = genes["speed"]
            self.vision_radius = genes["vision_radius"]
            self.eating_penalty = genes["eating_penalty"]
            self.health = genes["health"]
            self.hunger = genes["hunger"]
            self.lifespan = genes["lifespan"]
            self.reproduce_cycle = genes["reproduce_cycle"]
        self.genes = [
            self.speed,
            self.vision_radius,
            self.eating_penalty,
            self.health,
            self.hunger,
            self.lifespan,
            self.reproduce_cycle,
        ]

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

    def get_bit_array(self) -> Tuple[cp.ndarray, cp.ndarray]:
        bit_strs = (
            self.speed.get_bit_str(),
            self.vision_radius.get_bit_str(),
            self.eating_penalty.get_bit_str(),
            self.health.get_bit_str(),
            self.hunger.get_bit_str(),
            self.lifespan.get_bit_str(),
            self.reproduce_cycle.get_bit_str(),
        )
        bit_array_per_gene = cp.array(
            [[int(b) for b in bit_str] for bit_str in bit_strs]
        )
        bit_array = bit_array_per_gene.flatten()
        return bit_array, bit_array_per_gene

    def __str__(self) -> str:
        return self.get_bit_str()


def combined_genes(parent_1_genes, parent_2_genes):
    genes = {}
    for i in zip(parent_1_genes.genes, parent_2_genes.genes):
        ratio = random.random() * 1.1
        gene_value = i[0].float_value * ratio + i[1].float_value * max(1 - ratio, 0)
        gene = Gene(i[0].gene_type, value=gene_value)
        gene.mutate()
        genes[i[0].gene_type] = gene
    return Genes(genes)
