import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import zip_longest
from typing import List

from pymlga.chromosome import Chromosome, ChromosomeFactory


@dataclass
class Individual:
    chromosomes: List[Chromosome]

    def __post_init__(self):
        assert self.chromosomes
        assert None not in self.chromosomes

    def __iter__(self):
        return iter(self.chromosomes)


class IndividualFactory(ABC):

    @abstractmethod
    def spawn(self) -> Individual:  # pragma: no cover
        pass

    @abstractmethod
    def clone(self, individual: Individual) -> Individual:  # pragma: no cover
        pass

    @abstractmethod
    def crossover(self, individual1: Individual, individual2: Individual) -> Individual:  # pragma: no cover
        pass


@dataclass
class RandomMutatingIndividualFactory(IndividualFactory):

    chromosome_factory: ChromosomeFactory
    min_length: int = 1
    max_length: int = 1
    mutation_rate: float = 0
    shortening_rate: float = 0
    lengthening_rate: float = 0

    def __post_init__(self):
        assert self.min_length > 0
        assert self.max_length >= self.min_length
        assert self.mutation_rate >= 0
        assert self.mutation_rate <= 1
        assert self.shortening_rate >= 0
        assert self.shortening_rate <= 1
        assert self.lengthening_rate >= 0
        assert self.lengthening_rate <= 1

    def spawn(self) -> Individual:
        target_length = random.randint(self.min_length, self.max_length)
        chromosomes = [self.chromosome_factory.spawn() for _ in range(target_length)]
        return Individual(chromosomes=chromosomes)

    def clone(self, individual: Individual) -> Individual:
        chromosomes = [
            self.chromosome_factory.spawn() if (random.random() < self.mutation_rate) else self.chromosome_factory.clone(chromosome)
            for chromosome in individual.chromosomes
        ]
        lengthening = sum([
            (1 if random.random() < self.lengthening_rate and not random.random() < self.shortening_rate else 0)
            for _ in range(self.max_length - len(chromosomes))
        ])
        shortening = sum([
            (1 if random.random() < self.shortening_rate and not random.random() < self.lengthening_rate else 0)
            for _ in range(len(chromosomes) - self.min_length)
        ])
        target_length = len(chromosomes) + lengthening - shortening
        while len(chromosomes) > target_length:
            chromosomes.pop(random.randint(0, len(chromosomes) - 1))
        while len(chromosomes) < target_length:
            chromosomes.insert(random.randint(0, len(chromosomes)), self.chromosome_factory.spawn())
        return Individual(chromosomes=chromosomes)

    def crossover(self, individual1: Individual, individual2: Individual) -> Individual:
        return self.clone(Individual([
            random.choice([chromosome for chromosome in pair if chromosome is not None])
            for pair in zip_longest(individual1.chromosomes, individual2.chromosomes, fillvalue=None)
        ]))
