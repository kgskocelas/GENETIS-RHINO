import random
import unittest

from src.Genotype import Genotype
from src.Parameters import ParametersObject
from src.Phenotype import Phenotype
from src.WallPair import WallPair

cfg = ParametersObject("/Users/kgskocelas/PycharmProjects/GENETIS-RHINO/src/config.toml")

class PhenotypeTest(unittest.TestCase):
    """
    A test class to test the Phenotype class.
    """

    def test_constructor(self):
        """
        Tests the Phenotype constructor with valid inputs.
        """
        # Build a valid Genotype object.
        g = Genotype(cfg).generate(2, random.Random(1))

        # Build a valid Phenotype object.
        p = Phenotype(g, "Kate", "None", 0)

        self.assertIsInstance(p.genotype, Genotype)
        self.assertEqual(p.indv_id, "Kate")
        self.assertEqual(p.parent_id, "None")
        self.assertEqual(p.generation_created, 0)
        self.assertEqual(p.fitness_score, 880.3500822821234)

    def test_make_offspring(self):
        """Tests the make_offspring function."""
        # build valid parent phenotype
        g = Genotype(cfg).generate(2, random.Random(1))
        parent = Phenotype(g, "Kate", "None", 0)

        # make a single offspring via asexual reproduction
        child = parent.make_offspring("Oona", 1, random.Random(1))

        self.assertIsInstance(child.genotype, Genotype)
        self.assertEqual(child.indv_id, "Oona")
        self.assertEqual(child.parent_id, "Kate")
        self.assertEqual(child.generation_created, 1)
        self.assertEqual(child.fitness_score, 880.3086782506314)

if __name__ == '__main__':
    unittest.main()
