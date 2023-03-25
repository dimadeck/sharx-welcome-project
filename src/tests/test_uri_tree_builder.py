import pytest

from uri_tree_builder.exceptions import DifferentMethodsException


@pytest.mark.parametrize('input_list,expected', [
    (
            [
                ("GET", "/api/v1/cluster/metrics"),
                ("POST", "/api/v1/cluster/{cluster}/plugins"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")
            ],
            {'cluster': {'metrics': 'GET', 'plugins': 'POST'}}
    ),
    (
            [
                ("GET", "/api/v1/cluster/freenodes/list"),
                ("GET", "/api/v1/cluster/nodes"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                ("POST", "/api/v1/cluster/{cluster}/plugins")
            ],
            {'cluster': {'metrics': 'GET', 'plugins': 'POST', 'freenodes': {'list': 'GET'}, 'nodes': 'GET'}}
    )
])
def test_scenario_one_and_two(uri_tree_builder, input_list, expected):
    """
        Тест для первого и второго сценария из ТЗ.
        Так как uri_tree_builder - fixture для модуля, то значение tree для второго запуска сохраняется.

    :param uri_tree_builder: фикстура с экземпляром класса URITreeBuilder (одна на модуль)
    :param input_list: Входной список из ТЗ [(method, uri), ...]
    :param expected: Ожидаемый результат после выполнения метода построения дерева
    :return:
    """
    uri_tree_builder.build_tree(input_list)
    assert uri_tree_builder.tree == expected


@pytest.mark.xfail(raises=DifferentMethodsException)
def test_exception_different_methods(uri_tree_builder):
    """
        Тест, ожидающий вызова исключения DifferentMethodsException, так как при аналогичных ключах дерева,
        конечный метод отличается от предыдущего значения.
    :param uri_tree_builder: фикстура с экземпляром класса URITreeBuilder (одна на модуль)
    :return:
    """
    input_list = [
        ("POST", "/api/v1/cluster/freenodes/list")
    ]
    uri_tree_builder.build_tree(input_list)

