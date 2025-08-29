"""Class for constructing an antenna's Phenotype and acting upon it."""
import copy
import random
from typing import Optional

from src.CalcHornSize import CalcHornSize


class Phenotype:
    """
    Phenotype class.

    A wrapper for the Genotype class representing an individual antenna's
    phenotype.

    :param genotype: a Genotype instance.
    :type genotype: Genotype
    :param indv_id: The individual's unique ID.
    :type indv_id: str, optional
    :param parent_id: The individual's parent's unique ID.
    :type parent_id: str, optional
    :param generation_created: Which generation the individual was created.
    :type generation_created: int, optional
    :param fitness_score: The fitness score of the individual.
    :type fitness_score: float, optional
    """

    def __init__(self, genotype: object,
                 indv_id: Optional[str],
                 parent_id: Optional[str],
                 generation_created: Optional[int]) -> None:
        """
        Phenotype constructor.

        Constructs the phenotype of a genotype.

        :param genotype: a Genotype instance.
        :type genotype: Genotype
        :param indv_id: The individual's unique ID.
        :type indv_id: str, optional
        :param parent_id: The individual's parent's unique ID.
        :type parent_id: str, optional
        :param generation_created: Which generation the individual was created.
        :type generation_created: int, optional
        :rtype: None
        """
        self.genotype = genotype
        self.indv_id = indv_id
        self.parent_id = parent_id
        self.generation_created = generation_created
        self.fitness_score = CalcHornSize(genotype).fitness_score

    def make_offspring(self, new_id: str, generation_num: int,
                       rand: random.Random) -> object:
        """
        Make offspring.

        Makes an offspring from the individual Phenotype this is called on.

        :param new_id: The new individual's unique ID.
        :type new_id: str
        :param generation_num: The current generation number.
        :type generation_num: int
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        # make a copy of parent 1 to be the offspring
        offspring = copy.deepcopy(self)

        # set fields for new_indiv
        offspring.parent_id = self.indv_id
        offspring.indv_id = new_id
        offspring.generation_created = generation_num

        # mutate offspring
        offspring.genotype.mutate(rand)

        # calc new fitness score  TODO Replace with actual fitness calc
        offspring.fitness_score = CalcHornSize(offspring.genotype).fitness_score

        return offspring
