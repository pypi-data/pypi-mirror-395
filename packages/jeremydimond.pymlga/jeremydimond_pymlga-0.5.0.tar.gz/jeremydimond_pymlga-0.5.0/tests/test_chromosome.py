from typing import List, Callable
from unittest.mock import Mock, call, patch

import pytest
from pytesthelpers.exceptionhandling import does_not_raise, raises_assertion_error

from pymlga.allele import RepeatingQueueAlleleFactory
from pymlga.chromosome import Chromosome, FixedLengthChromosomeFactory, RandomLengthChromosomeFactory
from pymlga.gene import Gene, SimpleGeneFactory


def gene_factory():
    return SimpleGeneFactory(
        allele_factory=RepeatingQueueAlleleFactory(alleles=[
            f'spawned{index + 1}'
            for index in range(5)
        ])
    )


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


@pytest.mark.parametrize(
    argnames=['length', 'expected_exception'],
    argvalues=[
        (0, raises_assertion_error),
        (1, does_not_raise)
    ]
)
def test_fixed_length_chromosome_factory_constructor(length: int, expected_exception: Callable):
    with expected_exception():
        FixedLengthChromosomeFactory(gene_factory=gene_factory(), length=length)


def test_fixed_length_chromosome_factory_spawn():
    assert FixedLengthChromosomeFactory(gene_factory=gene_factory(), length=5).spawn() == Chromosome(genes=[Gene(allele='spawned1'),
                  Gene(allele='spawned2'),
                  Gene(allele='spawned3'),
                  Gene(allele='spawned4'),
                  Gene(allele='spawned5')
    ])


def test_fixed_length_chromosome_factory_clone():
    mock_genes = [Mock() for _ in range(5)]
    mock_gene_factory = Mock()
    mock_cloned_genes = [Mock() for _ in range(5)]
    mock_gene_factory.clone.side_effect = mock_cloned_genes
    assert FixedLengthChromosomeFactory(gene_factory=mock_gene_factory, length=5).clone(
        Chromosome(genes=mock_genes)
    ) == Chromosome(genes=mock_cloned_genes)
    assert mock_gene_factory.mock_calls == [
        call.clone(mock_gene)
        for mock_gene in mock_genes
    ]


@patch('random.choice', autospec=True)
def test_fixed_length_chromosome_factory_crossover(mock_choice: Mock):
    chromosome1 = Chromosome(genes=[Mock() for _ in range(5)])
    chromosome2 = Chromosome(genes=[Mock() for _ in range(5)])
    chosen = [
        chromosome2.genes[0],
        chromosome1.genes[1],
        chromosome1.genes[2],
        chromosome2.genes[3],
        chromosome1.genes[4]
    ]
    mock_choice.side_effect = chosen
    mock_gene_factory = Mock()
    mock_cloned_genes = [Mock() for _ in range(5)]
    mock_gene_factory.clone.side_effect = mock_cloned_genes
    assert FixedLengthChromosomeFactory(gene_factory=mock_gene_factory, length=5).crossover(
        chromosome1, chromosome2
    ) == Chromosome(genes=mock_cloned_genes)
    assert mock_gene_factory.mock_calls == [
        call.clone(gene)
        for gene in chosen
    ]


@pytest.mark.parametrize(
    argnames=['args', 'expected_exception'],
    argvalues=[
        ({}, does_not_raise),
        ({'shortening_rate': -0.01}, raises_assertion_error),
        ({'shortening_rate': 0}, does_not_raise),
        ({'shortening_rate': 0.5}, does_not_raise),
        ({'shortening_rate': 1}, does_not_raise),
        ({'shortening_rate': 1.01}, raises_assertion_error),
        ({'lengthening_rate': -0.01}, raises_assertion_error),
        ({'lengthening_rate': 0}, does_not_raise),
        ({'lengthening_rate': 0.5}, does_not_raise),
        ({'lengthening_rate': 1}, does_not_raise),
        ({'lengthening_rate': 1.01}, raises_assertion_error),
        ({'min_length': -1}, raises_assertion_error),
        ({'min_length': 0}, raises_assertion_error),
        ({'min_length': 1, 'max_length': 1}, raises_assertion_error),
        ({'min_length': 1, 'max_length': 2}, does_not_raise),
        ({'min_length': 1, 'max_length': 10}, does_not_raise),
        ({'min_length': 10, 'max_length': 10}, raises_assertion_error),
        ({'min_length': 11, 'max_length': 10}, raises_assertion_error),
    ]
)
def test_random_length_chromosome_factory_constructor(args: dict, expected_exception: Callable):
    with expected_exception():
        RandomLengthChromosomeFactory(**{
            **{'gene_factory': gene_factory(), 'min_length': 1, 'max_length': 2},
            **args
        })


@patch('random.randint', autospec=True)
def test_random_length_chromosome_factory_spawn(mock_randint: Mock):
    mock_randint.return_value = 7
    mock_gene_factory = Mock()
    mock_spawned_genes = [Mock() for _ in range(7)]
    mock_gene_factory.spawn.side_effect = mock_spawned_genes
    assert RandomLengthChromosomeFactory(
        gene_factory=mock_gene_factory,
        min_length=5,
        max_length=10,
        shortening_rate=0.5,
        lengthening_rate=0.5
    ).spawn() == Chromosome(genes=mock_spawned_genes)
    assert mock_gene_factory.mock_calls == 7 * [call.spawn()]


SHORTENING_RATE = 0.2
SHORTEN = SHORTENING_RATE - 0.1
DO_NOT_SHORTEN = SHORTENING_RATE
LENGTHENING_RATE = 0.8
LENGTHEN = LENGTHENING_RATE - 0.1
DO_NOT_LENGTHEN = LENGTHENING_RATE

@pytest.mark.parametrize(
    argnames=[
        'min_length',
        'max_length',
        'initial_length',
        'random_values',
        'randint_values',
        'expected_length'
    ],
    argvalues=[
        (1, 2, 1, [DO_NOT_LENGTHEN], [], 1),
        (1, 2, 1, [LENGTHEN], [0], 2),
        (1, 2, 1, [LENGTHEN], [1], 2),
        (1, 2, 2, [DO_NOT_SHORTEN], [], 2),
        (1, 2, 2, [SHORTEN], [0], 1),
        (5, 10, 7, 3*[DO_NOT_LENGTHEN]+2*[DO_NOT_SHORTEN], [], 7),
        (5, 10, 7, [LENGTHEN, DO_NOT_LENGTHEN, DO_NOT_LENGTHEN, DO_NOT_SHORTEN, SHORTEN], [], 7),
        (5, 10, 7, [LENGTHEN, DO_NOT_LENGTHEN, DO_NOT_LENGTHEN, SHORTEN, SHORTEN], [2], 6),
        (5, 10, 7, [LENGTHEN, LENGTHEN, DO_NOT_LENGTHEN, DO_NOT_SHORTEN, SHORTEN], [3], 8),
    ]
)
@patch('random.randint', autospec=True)
@patch('random.random', autospec=True)
def test_random_length_chromosome_factory_clone(
        mock_random: Mock,
        mock_randint: Mock,
        min_length: int,
        max_length: int,
        initial_length: int,
        random_values: List[float],
        randint_values: List[int],
        expected_length: int
):
    expected_add_count = max(0, expected_length - initial_length)
    expected_remove_count = max(0,  initial_length - expected_length)
    mock_random.side_effect = random_values
    mock_randint.side_effect = randint_values
    mock_initial_genes = [Mock() for _ in range(initial_length)]
    mock_gene_factory = Mock()
    mock_cloned_genes = [Mock() for _ in range(initial_length)]
    mock_gene_factory.clone.side_effect = mock_cloned_genes
    mock_spawned_genes = [Mock() for _ in range(expected_add_count)]
    mock_gene_factory.spawn.side_effect = mock_spawned_genes
    expected_genes = [gene for gene in mock_cloned_genes]
    for index in range(expected_add_count):
        expected_genes.insert(randint_values[index], mock_spawned_genes[index])
    for index in range(expected_remove_count):
        expected_genes.pop(randint_values[index])

    assert RandomLengthChromosomeFactory(
        gene_factory=mock_gene_factory,
        min_length=min_length,
        max_length=max_length,
        shortening_rate=SHORTENING_RATE,
        lengthening_rate=LENGTHENING_RATE
    ).clone(
        Chromosome(genes=mock_initial_genes)
    ) == Chromosome(genes=expected_genes)
    assert mock_gene_factory.mock_calls == [
        call.clone(mock_gene)
        for mock_gene in mock_initial_genes
    ] + [
        call.spawn()
        for _ in range(expected_add_count)
    ]
    assert mock_random.mock_calls == [call() for _ in random_values]
    assert mock_randint.mock_calls == [
        call(0, initial_length + index)
        for index in range(expected_add_count)
    ] + [
        call(0, initial_length - index - 1)
        for index in range(expected_remove_count)
    ]


@patch('pymlga.chromosome._clone', autospec=True)
@patch('random.choice', autospec=True)
def test_random_length_chromosome_factory_crossover(mock_choice: Mock, mock_clone: Mock):
    mock_chromosomes = [Mock() for _ in range(2)]
    gf = gene_factory()
    result = RandomLengthChromosomeFactory(
        gene_factory=gf,
        min_length=1,
        max_length=2,
        shortening_rate=SHORTENING_RATE,
        lengthening_rate=LENGTHENING_RATE
    ).crossover(*mock_chromosomes)
    assert mock_choice.mock_calls == [call(mock_chromosomes)]
    assert mock_clone.mock_calls == [call(
        chromosome=mock_choice.return_value,
        gene_factory=gf,
        min_length=1,
        max_length=2,
        shortening_rate=SHORTENING_RATE,
        lengthening_rate=LENGTHENING_RATE
    )]
    assert result == mock_clone.return_value
