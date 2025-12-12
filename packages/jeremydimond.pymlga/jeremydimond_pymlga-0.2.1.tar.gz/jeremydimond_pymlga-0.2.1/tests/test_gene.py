from typing import Callable
from unittest.mock import Mock, patch

import pytest
from pytesthelpers.exceptionhandling import raises_assertion_error, does_not_raise

from pymlga.gene import Gene, SimpleGeneFactory, RandomGeneFactory, RandomMutatingGeneFactory


@pytest.mark.parametrize(
    argnames=['allele', 'expected_exception'],
    argvalues=[
        (None, raises_assertion_error),
        ('something', does_not_raise)
    ]
)
def test_gene_validate(allele: str, expected_exception: Callable):
    with expected_exception():
        assert Gene(allele=allele).allele == allele


def test_simple_gene_factory():
    factory = SimpleGeneFactory(alleles=['one', 'two', 'three'])
    assert factory.clone(Gene(allele='one')) == Gene(allele='one')
    for _ in range(3):
        assert factory.spawn() == Gene(allele='one')
        assert factory.spawn() == Gene(allele='two')
        assert factory.spawn() == Gene(allele='three')


@patch('random.choice', autospec=True)
def test_random_gene_factory(mock_choice: Mock):
    factory = RandomGeneFactory(['one', 'two', 'three'])
    assert factory.clone(Gene(allele='one')) == Gene(allele='one')
    spawn_alleles = ["two", "three", "one", "two", "one"]
    mock_choice.side_effect = spawn_alleles
    for allele in spawn_alleles:
        assert factory.spawn() == Gene(allele=allele)


def test_gene_factory_requires_alleles():
    with raises_assertion_error():
        SimpleGeneFactory(alleles=[])
    with raises_assertion_error():
        RandomGeneFactory(alleles=[])
    with raises_assertion_error():
        RandomMutatingGeneFactory(alleles=[])


def test_gene_factory_mutation_rate_range():
    RandomMutatingGeneFactory(alleles=["x"], mutation_rate=0.0)
    RandomMutatingGeneFactory(alleles=["x"], mutation_rate=1.0)
    with raises_assertion_error():
        RandomMutatingGeneFactory(alleles=["x"], mutation_rate=-0.01)
    with raises_assertion_error():
        RandomMutatingGeneFactory(alleles=["x"], mutation_rate=1.01)

@patch('random.choice', autospec=True)
def test_random_mutating_gene_factory_spawn(mock_choice: Mock):
    spawn_alleles = ["two", "three", "one", "two", "one"]
    mock_choice.side_effect = spawn_alleles
    factory = RandomMutatingGeneFactory(['one', 'two', 'three'])
    for allele in spawn_alleles:
        assert factory.spawn() == Gene(allele=allele)


def test_random_mutating_gene_factory_clone_mutate_never():
    factory = RandomMutatingGeneFactory(['one', 'two', 'three'])
    assert factory.clone(Gene(allele='one')) == Gene(allele='one')


@patch('random.choice', autospec=True)
def test_random_mutating_gene_factory_clone_mutate_always(mock_choice: Mock):
    spawn_alleles = ["two", "three", "one", "two", "one"]
    mock_choice.side_effect = spawn_alleles
    factory = RandomMutatingGeneFactory(
        alleles=['one', 'two', 'three'],
        mutation_rate=1.0
    )
    for allele in spawn_alleles:
        assert factory.clone(Gene(allele='one')) == Gene(allele=allele)


@patch('random.choice', autospec=True)
@patch('random.random', autospec=True)
def test_random_mutating_gene_factory_clone_mutate_sometimes(mock_random: Mock, mock_choice: Mock):
    spawn_alleles = ["two", "three", "one", "two", "one"]
    mock_choice.side_effect = spawn_alleles
    mock_random.side_effect = [0.999, 0.51, 0.5, 0.4999, 0.3, 0.2, 0.1, 0.0]
    factory = RandomMutatingGeneFactory(
        alleles=['one', 'two', 'three'],
        mutation_rate=0.5
    )
    for _ in range(3):
        assert factory.clone(Gene(allele='one')) == Gene(allele='one')
    for allele in spawn_alleles:
        assert factory.clone(Gene(allele='one')) == Gene(allele=allele)

