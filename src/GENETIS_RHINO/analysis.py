"""Record the best individuals and fitness score statistics for each generation of Phenotypes."""
from pathlib import Path

import pandas as pd

from src.GENETIS_RHINO.phenotype import Phenotype


class Analysis:
    """Collect data about the progress of generations and fitness."""

    def __init__(self, population: list) -> None:
        """Track the population as it is updated."""
        self.population = population
        self.generation_counter = 0

    def update(self, generation_num: int) -> None:
        """Increment the generation counter; write to the fitness and the best individual CSV files."""
        self.generation_counter = generation_num
        print(f"Generation: {self.generation_counter}")
        self.update_fitness_scores()
        self.update_best_individuals()

    def update_best_individuals(self) -> list[Phenotype]:
        """Read the nsgaii rank from each individual and find the individuals on the pareto front (lowest rank)."""
        min_rank = min(indv.nsgaii_rank for indv in self.population)
        best_indvs = [indv for indv in self.population if indv.nsgaii_rank==min_rank]
        self.to_csv_best_individuals(best_indvs)
        return best_indvs

    def to_csv_best_individuals(self,
                                best_indvs: list[Phenotype],
                                csv_path: str="best_individuals.csv") -> None:
        """Write the attributes of the best phenotypes to a CSV file."""

        def make_row(indv: Phenotype) -> pd.DataFrame:
            """Get the attributes of a phenotype and turn its attributes into a table row."""
            row = {}
            row["Indiv_ID"]                   = [indv.indv_id]
            row["Parent1_ID"]            = [indv.parent1_id]
            row["Generation_Created"]   = [indv.generation_created]
            row["Flare_Length"]         = [indv.genotype.flare_length]
            row["Waveguide_Height"]     = [indv.genotype.waveguide_height]
            row["Waveguide_Length"]     = [indv.genotype.waveguide_length]
            row["Waveguide_Width"]      = [indv.genotype.waveguide_width]

            counter = 1
            for wp in indv.genotype.walls:
                attribute = "WP" + str(counter) + "_Has_Ridge"
                row[attribute] = [wp.has_ridge]

                attribute = "WP" + str(counter) + "_Angle"
                row[attribute] = [wp.angle]

                attribute = "WP" + str(counter) + "_Ridge_Height"
                row[attribute] = [wp.ridge_height]

                attribute = "WP" + str(counter) + "_Ridge_Width_Top"
                row[attribute] = [wp.ridge_width_top]

                attribute = "WP" + str(counter) + "_Ridge_Width_Bottom"
                row[attribute] = [wp.ridge_width_bottom]

                attribute = "WP" + str(counter) + "_Ridge_Thickness_Top"
                row[attribute] = [wp.ridge_thickness_top]

                attribute = "WP" + str(counter) + "_Ridge_Thickness_Bottom"
                row[attribute] = [wp.ridge_thickness_bottom]

                counter += 1

            for metric, score in indv.fitness_scores.items():
                row[metric] = [score]
            return pd.DataFrame(row)

        indv_df = pd.concat([make_row(indv) for indv in best_indvs])
        indv_df.to_csv(csv_path, mode="w", header=True, index=False)
        return indv_df

    def update_fitness_scores(self) -> dict[str, int]:
        """Read the fitness from each individual and calculate the maximum and average."""
        # Create dictionary containing fitness scores from every phenotype in the population.
        all_scores = {}
        for indv in self.population:
            scores = indv.fitness_scores
            # Append the fitness scores for each individual to the all_score dictionary.
            if len(all_scores) > 0:
                for metric, score in scores.items():
                    all_scores[metric].append(score)
            # On the first phenotype of the population, initiate the all_score dictionary.
            else:
                all_scores = {metric: [score] for metric, score in scores.items()}
        # Create the fitness statistics log.
        fitness_stats_dict = {"Generation": self.generation_counter}
        for metric, scores in all_scores.items():
            fitness_stats_dict[metric+"_Average"] = [sum(scores) / len(scores)]
            fitness_stats_dict[metric+"_Maximum"] = [max(scores)]
        self.to_csv_fitness(fitness_stats_dict)
        return fitness_stats_dict

    def to_csv_fitness(self, fitness: dict, csv_path: str="fitness.csv") -> pd.DataFrame:
        """Write generation fitness statistics to a CSV file."""
        # Format data for CSV using pandas.
        fitness_row = pd.DataFrame(fitness)
        fitness_row.to_csv(csv_path, mode="a", header=not Path(csv_path).exists(), index=False)
        return fitness_row
