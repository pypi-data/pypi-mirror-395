from dataclasses import dataclass
from typing import List, Callable
from unittest.mock import Mock, patch, call

import pytest
from pytesthelpers.exceptionhandling import does_not_raise, raises_assertion_error

from pymlga.chromosome import Chromosome, RandomMutatingChromosomeFactory
from pymlga.gene import Gene, SimpleGeneFactory


@pytest.mark.parametrize(
    argnames=['genes', 'expected_exception'],
    argvalues=[
        (None, raises_assertion_error),
        ([], does_not_raise),
        ([Gene("x"), None, Gene("y")], raises_assertion_error),
        ([Gene("x")], does_not_raise)
    ]
)
def test_chromosome_validate(genes: List[Gene], expected_exception: Callable):
    with expected_exception():
        assert Chromosome(genes=genes).genes == genes


def test_chromosome_iterable():
    genes = [
        Gene(allele='one'),
        Gene(allele='two'),
        Gene(allele='three')
    ]
    result = [gene for gene in Chromosome(genes=genes)]
    assert result == genes

FACTORY_CREATE_ARGS = {'gene_factory': SimpleGeneFactory(['x'])}
@pytest.mark.parametrize(
    ids=lambda param: str(param),
    argnames=['args', 'expected_exception'],
    argvalues=[
        (FACTORY_CREATE_ARGS, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'min_length': 0}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'min_length': 1}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'min_length': 2}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'min_length': 2, 'max_length': 2}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'mutation_rate': 0}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'mutation_rate': -0.01}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'mutation_rate': 1}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'mutation_rate': 1.01}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'shortening_rate': 0}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'shortening_rate': -0.01}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'shortening_rate': 1}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'shortening_rate': 1.01}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'lengthening_rate': 0}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'lengthening_rate': -0.01}, raises_assertion_error),
        ({**FACTORY_CREATE_ARGS, 'lengthening_rate': 1}, does_not_raise),
        ({**FACTORY_CREATE_ARGS, 'lengthening_rate': 1.01}, raises_assertion_error)
    ]
)
def test_factory_creation_validation(args: dict, expected_exception: Callable):
    with expected_exception():
        RandomMutatingChromosomeFactory(**args)


@patch('random.randint', autospec=True)
def test_random_mutating_chromosome_factory_spawn(mock_randint: Mock):
    mock_randint.side_effect = [3, 2, 1]
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three']),
        min_length=2,
        max_length=10
    )
    assert factory.spawn() == Chromosome(genes=[Gene(allele='one'), Gene(allele='two'), Gene(allele='three')])
    assert factory.spawn() == Chromosome(genes=[Gene(allele='one'), Gene(allele='two')])
    assert factory.spawn() == Chromosome(genes=[Gene(allele='three')])
    assert mock_randint.mock_calls == 3 * [call(2, 10)]


def test_random_mutating_chromosome_factory_clone_never_mutate():
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three'])
    )
    assert factory.clone(Chromosome(genes=[Gene('two')])) == Chromosome(genes=[Gene('two')])


def test_random_mutating_chromosome_factory_clone_always_mutate():
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three']),
        mutation_rate=1.0
    )
    assert factory.clone(Chromosome(genes=[Gene('two')])) == Chromosome(genes=[Gene('one')])
    assert factory.clone(Chromosome(genes=[Gene('two')])) == Chromosome(genes=[Gene('two')])
    assert factory.clone(Chromosome(genes=[Gene('two')])) == Chromosome(genes=[Gene('three')])


def test_random_mutating_chromosome_factory_clone_always_lengthen():
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three']),
        min_length=1,
        max_length=3,
        lengthening_rate=1.0
    )
    assert len(factory.clone(Chromosome(genes=[Gene('two')])).genes) == 3


def test_random_mutating_chromosome_factory_clone_always_shorten():
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three']),
        min_length=1,
        max_length=3,
        shortening_rate=1.0
    )
    assert len(factory.clone(Chromosome(genes=[Gene('one'), Gene('two'), Gene('three')])).genes) == 1


def test_random_mutating_chromosome_factory_clone_always_shorten_and_lengthen():
    factory = RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory(['one', 'two', 'three']),
        min_length=1,
        max_length=3,
        shortening_rate=1.0,
        lengthening_rate=1.0
    )
    for chromosome in [
        Chromosome(genes=[Gene('one')]),
        Chromosome(genes=[Gene('one'), Gene('two')]),
        Chromosome(genes=[Gene('one'), Gene('two'), Gene('three')]),
    ]:
        assert factory.clone(chromosome) == chromosome


@dataclass
class CloneWithMutationsParam:
    description: str
    chromosome: Chromosome
    mutation_rate: float
    shortening_rate: float
    lengthening_rate: float
    random_side_effect: List[float]
    randint_side_effect: List[int]
    expected_result: Chromosome
    expected_random_call_count: int
    expected_randint_call_args: List[int]

@pytest.mark.parametrize(
    ids=lambda param: param.description,
    argnames='param',
    argvalues=[
        CloneWithMutationsParam(
            description='mutate and lengthen',
            chromosome=Chromosome([Gene('one'), Gene('two')]),
            mutation_rate=0.1,
            shortening_rate=0.3,
            lengthening_rate=0.2,
            random_side_effect=[
                0.09,       # mutate
                0.1,        # don't mutate
                0.19, 0.3,  # lengthen don't shorten (+1)
                0.2,        # don't lengthen
                0.19, 0.29, # lengthen and shorten
                0.1, 0.31,  # lengthen don't shorten (+1)
                0.19, 0.3,  # lengthen don't shorten (+1)
                0.19, 0.3,  # lengthen don't shorten (+1)
                0.29, 0.2,  # shorten don't lengthen (-1)
            ],
            randint_side_effect=[1, 0, 4],
            expected_result=Chromosome([
                Gene('spawned3'), # added
                Gene('spawned1'), # mutated
                Gene('spawned2'), # added
                Gene('two'),      # original
                Gene('spawned4')  # added
            ]),
            expected_random_call_count=15,
            expected_randint_call_args=[2, 3, 4]
        ),
        CloneWithMutationsParam(
            description='mutate and shrink',
            chromosome=Chromosome([Gene('one'), Gene('two'), Gene('three'), Gene('four'), Gene('five')]),
            mutation_rate=0.1,
            shortening_rate=0.3,
            lengthening_rate=0.2,
            random_side_effect=[
                0.1,        # don't mutate
                0.09,       # mutate
                0.01,       # mutate
                0.11,       # don't mutate
                0.11,       # don't mutate
                0.19, 0.3,  # lengthen don't shorten (+1)
                0.19, 0.29, # lengthen and shorten
                0.2,        # don't lengthen
                0.29, 0.2,  # shorten don't lengthen (-1)
                0.29, 0.2,  # shorten don't lengthen (-1)
                0.29, 0.2,  # shorten don't lengthen (-1)
                0.29, 0.2,  # shorten don't lengthen (-1)
            ],
            randint_side_effect=[1, 3, 0],
            expected_result=Chromosome([
                #Gene('one'),       # original, removed
                # Gene('spawned1'), # mutated, removed
                Gene('spawned2'),  # mutated
                Gene('four'),      # original
                #Gene('five')      # original, removed
            ]),
            expected_random_call_count=18,
            expected_randint_call_args=[4, 3, 2]
        ),
    ]
)
@patch('random.randint', autospec=True)
@patch('random.random', autospec=True)
def test_random_mutating_chromosome_factory_clone_with_mutations(
        mock_random: Mock,
        mock_randint: Mock,
        param: CloneWithMutationsParam
):
    mock_random.side_effect = param.random_side_effect
    mock_randint.side_effect = param.randint_side_effect
    assert RandomMutatingChromosomeFactory(
        gene_factory=SimpleGeneFactory([f'spawned{(i+1)}' for i in range(10)]),
        min_length=1,
        max_length=8,
        mutation_rate=param.mutation_rate,
        shortening_rate=param.shortening_rate,
        lengthening_rate=param.lengthening_rate
    ).clone(param.chromosome) == param.expected_result
    assert mock_random.mock_calls == param.expected_random_call_count * [call()]
    assert mock_randint.mock_calls == [
        call(0, arg)
        for arg in param.expected_randint_call_args
    ]

@patch('random.choice', autospec=True)
def test_random_mutating_chromosome_factory_crossover_never_mutate(mock_choice: Mock):
    factory = RandomMutatingChromosomeFactory(gene_factory=SimpleGeneFactory(['blah']))
    chromosome1 = Chromosome(genes=[Gene('one')])
    chromosome2 = Chromosome(genes=[Gene('two')])
    choices = 2 * [chromosome1, chromosome2]
    mock_choice.side_effect = choices
    for choice in choices:
        assert factory.crossover(chromosome1, chromosome2) == choice
