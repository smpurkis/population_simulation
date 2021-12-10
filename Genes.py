import numpy as np


class Genes(object):
    def __init__(self):
        self.speed = self.get_random_gene_value(1.0, 1.0, 0.5, 1.5)
        self.vision_radius = self.get_random_gene_value(1.0, 0.5, 0.25, 2.0)
        self.eating_penalty = self.get_random_gene_value(1.0, 1.0, 0.5, 2.0)
        self.health = self.get_random_gene_value(1.0, 0.5, 0.25, 2.0)
        self.hunger = self.get_random_gene_value(1.0, 0.5, 0.25, 2.0)
        self.lifespan = self.get_random_gene_value(1.0, 0.5, 0.25, 2.0)
        self.reproduce_cycle = self.get_random_gene_value(1.0, 1.0, 0.5, 2.0)

    @staticmethod
    def get_random_gene_value(
        mean: float, std: float, min_value: float = 0.5, max_value: float = 1.5
    ):
        value = float(np.random.normal(mean, std))
        if value < min_value:
            value = min_value
        if value > max_value:
            value = max_value
        return value
