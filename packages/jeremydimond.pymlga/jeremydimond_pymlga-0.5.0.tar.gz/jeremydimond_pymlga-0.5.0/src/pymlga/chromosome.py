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
class FixedLengthChromosomeFactory(ChromosomeFactory):

    gene_factory: GeneFactory
    length: int = 1

    def __post_init__(self):
        assert self.length > 0

    def spawn(self) -> Chromosome:
        return Chromosome(genes=[
            self.gene_factory.spawn()
            for _ in range(self.length)
        ])

    def clone(self, chromosome: Chromosome) -> Chromosome:
        return Chromosome(genes=[
            self.gene_factory.clone(gene)
            for gene in chromosome
        ])

    def crossover(self, chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
        return Chromosome(genes=[
            self.gene_factory.clone(random.choice(genes))
            for genes in zip(chromosome1.genes, chromosome2.genes)
        ])


@dataclass
class RandomLengthChromosomeFactory(ChromosomeFactory):

    gene_factory: GeneFactory
    min_length: int
    max_length: int
    shortening_rate: float = 0
    lengthening_rate: float = 0

    def __post_init__(self):
        assert self.min_length > 0
        assert self.max_length > self.min_length
        assert self.shortening_rate >= 0
        assert self.shortening_rate <= 1
        assert self.lengthening_rate >= 0
        assert self.lengthening_rate <= 1

    def spawn(self) -> Chromosome:
        return Chromosome(genes=[
            self.gene_factory.spawn()
            for _ in range(random.randint(self.min_length, self.max_length))
        ])

    def clone(self, chromosome: Chromosome) -> Chromosome:
        return _clone(
            chromosome=chromosome,
            gene_factory=self.gene_factory,
            min_length=self.min_length,
            max_length=self.max_length,
            shortening_rate=self.shortening_rate,
            lengthening_rate=self.lengthening_rate
        )

    def crossover(self, chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
        return _clone(
            chromosome=random.choice([chromosome1, chromosome2]),
            gene_factory=self.gene_factory,
            min_length=self.min_length,
            max_length=self.max_length,
            shortening_rate=self.shortening_rate,
            lengthening_rate=self.lengthening_rate
        )


def _clone(
        chromosome: Chromosome,
        gene_factory: GeneFactory,
        min_length: int,
        max_length: int,
        shortening_rate: float,
        lengthening_rate: float
) -> Chromosome:
    genes = [
        gene_factory.clone(gene)
        for gene in chromosome.genes
    ]
    lengthening = sum([
        (1 if random.random() < lengthening_rate else 0)
        for _ in range(max_length - len(genes))
    ])
    shortening = sum([
        (1 if random.random() < shortening_rate else 0)
        for _ in range(len(genes) - min_length)
    ])
    target_length = len(genes) + lengthening - shortening
    while len(genes) > target_length:
        genes.pop(random.randint(0, len(genes) - 1))
    while len(genes) < target_length:
        genes.insert(random.randint(0, len(genes)), gene_factory.spawn())
    return Chromosome(genes=genes)
