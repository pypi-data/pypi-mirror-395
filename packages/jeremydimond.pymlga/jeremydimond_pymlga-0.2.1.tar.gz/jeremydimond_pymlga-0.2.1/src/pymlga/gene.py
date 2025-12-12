import random
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import List

@dataclass
class Gene:

    allele: str

    def __post_init__(self):
        assert self.allele is not None


class GeneFactory(ABC):
    @abstractmethod
    def spawn(self) -> Gene:  # pragma: no cover
        pass

    @abstractmethod
    def clone(self, gene: Gene) -> Gene:  # pragma: no cover
        pass

@dataclass
class SimpleGeneFactory(GeneFactory):
    alleles: List[str]
    _index: int = field(default=-1, init=False)

    def __post_init__(self):
        assert self.alleles

    def spawn(self) -> Gene:
        self._index = (self._index + 1) % len(self.alleles)
        return Gene(allele=self.alleles[self._index])

    def clone(self, gene: Gene) -> Gene:
        return Gene(allele=gene.allele)


@dataclass
class RandomGeneFactory(SimpleGeneFactory):

    def spawn(self) -> Gene:
        return Gene(allele=random.choice(self.alleles))

@dataclass
class RandomMutatingGeneFactory(RandomGeneFactory):

    mutation_rate: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        assert self.mutation_rate >= 0
        assert self.mutation_rate <= 1

    def clone(self, gene: Gene) -> Gene:
        if random.random() < self.mutation_rate:
            return self.spawn()
        return super().clone(gene=gene)

