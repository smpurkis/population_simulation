import numpy as np


class Genes(object):
    def __init__(self):
        gene_ratio = gr = np.random.normal(1.0, 0.25, 5)
        gr[gr < 0.1] = 0.5
        gr[gr > 1.5] = 1.5
        self.speed = float(gene_ratio[0])
        self.vision_radius = float(gene_ratio[1])
        self.eating_penalty = float(gene_ratio[2])
        self.health = float(gene_ratio[3])
        self.hunger = float(gene_ratio[4])
