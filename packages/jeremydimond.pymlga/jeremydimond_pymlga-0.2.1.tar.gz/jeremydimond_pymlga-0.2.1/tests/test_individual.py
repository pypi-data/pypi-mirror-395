from dataclasses import dataclass
from typing import List, Callable
from unittest.mock import patch, Mock, create_autospec, call

import pytest
from pytesthelpers.exceptionhandling import raises_assertion_error, does_not_raise

from pymlga.chromosome import Chromosome, RandomMutatingChromosomeFactory, ChromosomeFactory
from pymlga.gene import Gene, SimpleGeneFactory
from pymlga.individual import Individual, RandomMutatingIndividualFactory


def test_iterable():
    individual = Individual(chromosomes=[
        Chromosome(genes=[Gene('one')]),
        Chromosome(genes=[Gene('one'), Gene('two')]),
        Chromosome(genes=[Gene('two'), Gene('three')])
    ])
    assert [c for c in individual] == individual.chromosomes


@pytest.mark.parametrize(
    argnames=['chromosomes', 'expected_exception'],
    argvalues=[
        (None, raises_assertion_error),
        ([], raises_assertion_error),
        ([Chromosome([Gene("x")]), None, Chromosome([Gene("y")])], raises_assertion_error),
        ([Chromosome([Gene("x")])], does_not_raise)
    ]
)
def test_individual_validate(chromosomes: List[Chromosome], expected_exception: Callable):
    with expected_exception():
        assert Individual(chromosomes=chromosomes).chromosomes == chromosomes


FACTORY_CREATE_ARGS = {'chromosome_factory': RandomMutatingChromosomeFactory(SimpleGeneFactory(["x"]))}
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
        RandomMutatingIndividualFactory(**args)


@patch('random.randint', autospec=True)
def test_random_mutating_individual_factory_spawn(mock_randint: Mock):
    mock_randint.return_value = 3
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosomes = 3 * [create_autospec(spec=Chromosome)]
    mock_chromosome_factory.return_value.spawn.side_effect = mock_chromosomes
    factory = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        min_length=2,
        max_length=10
    )
    assert factory.spawn().chromosomes == mock_chromosomes
    assert mock_randint.mock_calls == [call(2, 10)]
    assert mock_chromosome_factory.mock_calls == 3 * [call().spawn()]


def test_random_mutating_individual_factory_clone_never_mutate():
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosomes = 3 * [create_autospec(spec=Chromosome)]
    mock_chromosome_factory.return_value.clone.side_effect = mock_chromosomes
    individual = Individual(chromosomes=[
        Chromosome(genes=[Gene('x')]),
        Chromosome(genes=[Gene('y')]),
        Chromosome(genes=[Gene('z')])
    ])

    factory = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value
    )
    assert factory.clone(individual).chromosomes == mock_chromosomes
    assert mock_chromosome_factory.mock_calls == [
        call().clone(chromosome)
        for chromosome in individual.chromosomes
    ]


def test_random_mutating_individual_factory_clone_always_mutate():
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosomes = 3 * [create_autospec(spec=Chromosome)]
    mock_chromosome_factory.return_value.spawn.side_effect = mock_chromosomes
    individual = Individual(chromosomes=[
        Chromosome(genes=[Gene('x')]),
        Chromosome(genes=[Gene('y')]),
        Chromosome(genes=[Gene('z')])
    ])

    factory = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        mutation_rate=1.0
    )
    assert factory.clone(individual).chromosomes == mock_chromosomes
    assert mock_chromosome_factory.mock_calls == 3 * [call().spawn()]


def test_random_mutating_individual_factory_clone_always_lengthen():
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosomes = 3 * [create_autospec(spec=Chromosome)]
    mock_chromosome_factory.return_value.spawn.side_effect = mock_chromosomes
    individual = Individual(chromosomes=[
        Chromosome(genes=[Gene('x')]),
        Chromosome(genes=[Gene('y')]),
        Chromosome(genes=[Gene('z')])
    ])

    factory = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        min_length=1,
        max_length=3,
        lengthening_rate=1.0
    )
    assert len(factory.clone(individual).chromosomes) == 3


def test_random_mutating_individual_factory_clone_always_shorten():
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosomes = 3 * [create_autospec(spec=Chromosome)]
    mock_chromosome_factory.return_value.spawn.side_effect = mock_chromosomes
    individual = Individual(chromosomes=[
        Chromosome(genes=[Gene('x')]),
        Chromosome(genes=[Gene('y')]),
        Chromosome(genes=[Gene('z')])
    ])

    factory = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        min_length=1,
        max_length=3,
        shortening_rate=1.0
    )
    assert len(factory.clone(individual).chromosomes) == 1


def test_random_mutating_individual_factory_clone_always_shorten_and_lengthen():
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
    individual: Individual
    mutation_rate: float
    shortening_rate: float
    lengthening_rate: float
    random_side_effect: List[float]
    randint_side_effect: List[int]
    expected_result: Individual
    expected_random_call_count: int
    expected_randint_call_args: List[int]
    expected_chromosome_factory_calls: list

@pytest.mark.parametrize(
    ids=lambda param: param.description,
    argnames='param',
    argvalues=[
        CloneWithMutationsParam(
            description='mutate and lengthen',
            individual=Individual([
                Chromosome([Gene('one')]),
                Chromosome([Gene('two')])
            ]),
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
            expected_result=Individual([
                Chromosome([Gene('spawned3')]), # added
                Chromosome([Gene('spawned1')]), # mutated
                Chromosome([Gene('spawned2')]), # added
                Chromosome([Gene('cloned from two')]),      # original
                Chromosome([Gene('spawned4')])  # added
            ]),
            expected_random_call_count=15,
            expected_randint_call_args=[2, 3, 4],
            expected_chromosome_factory_calls=[
                call().spawn(),
                call().clone(Chromosome(genes=[Gene(allele='two')])),
                call().spawn(),
                call().spawn(),
                call().spawn()
            ]
        ),
        CloneWithMutationsParam(
            description='mutate and shrink',
            individual=Individual([
                Chromosome([Gene('one')]),
                Chromosome([Gene('two')]),
                Chromosome([Gene('three')]),
                Chromosome([Gene('four')]),
                Chromosome([Gene('five')])
            ]),
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
            expected_result=Individual([
                Chromosome([Gene('spawned2')]),
                Chromosome([Gene('cloned from four')])
            ]),
            expected_random_call_count=18,
            expected_randint_call_args=[4, 3, 2],
            expected_chromosome_factory_calls=[
                call().clone(Chromosome(genes=[Gene(allele='one')])),
                call().spawn(),
                call().spawn(),
                call().clone(Chromosome(genes=[Gene(allele='four')])),
                call().clone(Chromosome(genes=[Gene(allele='five')]))
            ]
        ),
    ]
)
@patch('random.randint', autospec=True)
@patch('random.random', autospec=True)
def test_random_mutating_individual_factory_clone_with_mutations(
        mock_random: Mock,
        mock_randint: Mock,
        param: CloneWithMutationsParam
):
    mock_random.side_effect = param.random_side_effect
    mock_randint.side_effect = param.randint_side_effect
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosome_factory.return_value.spawn.side_effect = [
        Chromosome(genes=[Gene(f'spawned{i+1}')])
        for i in range(10)
    ]
    mock_chromosome_factory.return_value.clone.side_effect = lambda chromosome: Chromosome([
        Gene(f'cloned from {chromosome.genes[0].allele}')
    ])
    assert RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        min_length=1,
        max_length=8,
        mutation_rate=param.mutation_rate,
        shortening_rate=param.shortening_rate,
        lengthening_rate=param.lengthening_rate
    ).clone(param.individual) == param.expected_result
    assert mock_random.mock_calls == param.expected_random_call_count * [call()]
    assert mock_randint.mock_calls == [
        call(0, arg)
        for arg in param.expected_randint_call_args
    ]
    assert mock_chromosome_factory.mock_calls == param.expected_chromosome_factory_calls

@patch('random.choice', autospec=True)
def test_random_mutating_individual_factory_crossover_never_mutate(mock_choice: Mock):
    individual1 = Individual([
        Chromosome([Gene('101')]),
        Chromosome([Gene('102')]),
        Chromosome([Gene('103')]),
    ])
    individual2 = Individual([
        Chromosome([Gene('201')]),
        Chromosome([Gene('202')]),
    ])
    mock_choice.side_effect = [
        Chromosome([Gene('101')]),
        Chromosome([Gene('202')]),
        Chromosome([Gene('103')])
    ]
    mock_chromosome_factory = create_autospec(spec=ChromosomeFactory)
    mock_chromosome_factory.return_value.clone.side_effect = lambda chromosome: Chromosome([
        Gene(f'cloned from {chromosome.genes[0].allele}')
    ])
    result = RandomMutatingIndividualFactory(
        chromosome_factory=mock_chromosome_factory.return_value,
        min_length=2,
        max_length=3
    ).crossover(individual1, individual2)

    assert mock_choice.mock_calls == [
        call([Chromosome([Gene('101')]), Chromosome([Gene('201')])]),
        call([Chromosome([Gene('102')]), Chromosome([Gene('202')])]),
        call([Chromosome([Gene('103')])])
    ]

    assert result == Individual([
        Chromosome([Gene('cloned from 101')]),
        Chromosome([Gene('cloned from 202')]),
        Chromosome([Gene('cloned from 103')])
    ])
