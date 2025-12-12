import random
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List

from pymlga.gene import Gene, GeneFactory


@dataclass
class Chromosome:
    genes: List[Gene]

    def __post_init__(self):
        assert self.genes is not None
        assert None not in self.genes

    def __iter__(self):
        return iter(self.genes)


class ChromosomeFactory(ABC):

    @abstractmethod
    def spawn(self) -> Chromosome:  # pragma: no cover
        pass

    @abstractmethod
    def clone(self, chromosome: Chromosome) -> Chromosome:  # pragma: no cover
        pass

    @abstractmethod
    def crossover(self, chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:  # pragma: no cover
        pass


@dataclass
class RandomMutatingChromosomeFactory(ChromosomeFactory):

    gene_factory: GeneFactory
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

    def spawn(self) -> Chromosome:
        target_length = random.randint(self.min_length, self.max_length)
        genes = [self.gene_factory.spawn() for _ in range(target_length)]
        return Chromosome(genes=genes)

    def clone(self, chromosome: Chromosome) -> Chromosome:
        genes = [
            self.gene_factory.spawn() if (random.random() < self.mutation_rate) else self.gene_factory.clone(gene)
            for gene in chromosome.genes
        ]
        lengthening = sum([
            (1 if random.random() < self.lengthening_rate and not random.random() < self.shortening_rate else 0)
            for _ in range(self.max_length - len(genes))
        ])
        shortening = sum([
            (1 if random.random() < self.shortening_rate and not random.random() < self.lengthening_rate else 0)
            for _ in range(len(genes) - self.min_length)
        ])
        target_length = len(genes) + lengthening - shortening
        while len(genes) > target_length:
            genes.pop(random.randint(0, len(genes) - 1))
        while len(genes) < target_length:
            genes.insert(random.randint(0, len(genes)), self.gene_factory.spawn())
        return Chromosome(genes=genes)

    def crossover(self, chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
        return self.clone(random.choice([chromosome1, chromosome2]))
