from dataclasses import dataclass
from typing import List

from pymlga.evaluation import EvaluatedIndividual


@dataclass
class Generation:
    generation_number: int
    ranked_individuals: List[EvaluatedIndividual]
    size: int
    top_fitness: float
    average_fitness: float
    bottom_fitness: float
    sum_fitness: float
    fittest: EvaluatedIndividual
