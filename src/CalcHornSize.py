"""Class to calculate the size of a horn antenna. Size of horn is used as
the fitness score of a phenotype in the software's first phase to make sure
everything is working."""
from src.Genotype import Genotype


class CalcHornSize:
    """CalcHornSize class"""

    def __init__(self, genotype: Genotype) -> None:
        """constructor"""
        self.fitness_score = genotype.flare_length + genotype.waveguide_height
