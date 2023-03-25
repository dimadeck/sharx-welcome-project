from typing import List, Generator

from uri_tree_builder.exceptions import DifferentMethodsException
from uri_tree_builder.ignore_rules import APIWordIgnoreRule, V1WordIgnoreRule, CommandIgnoreRule, EmptyIgnoreRule


class URITreeBuilder:
    """
    Класс для построения дерева URI
    input_list = [
                ("GET", "/api/v1/cluster/metrics"),
                ("POST", "/api/v1/cluster/{cluster}/plugins"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")
            ]
    uri_tree_builder = URITreeBuilder()
    tree = uri_tree_builder.build_tree(input_list)

    print(tree)
    # Или
    print(uri_tree_builder.tree)
    >> {'cluster': {'metrics': 'GET', 'plugins': 'POST'}}
    """
    IGNORE_LIST = [APIWordIgnoreRule, V1WordIgnoreRule, CommandIgnoreRule, EmptyIgnoreRule]

    def __init__(self):
        self._tree = {}

    @property
    def tree(self) -> dict:
        return self._tree

    def build_tree(self, input_list: List) -> dict:
        """
        Интерфейсный метод для заполнения/обновления дерева путей (URI)
        :param input_list: входной лист со структурами: (method, uri)
        :return: Обновленное дерево URI
        """
        for method, uri in input_list:
            breadcrumbs = self._parse_uri(uri)
            current_branch = self._tree
            for breadcrumb in breadcrumbs:
                if breadcrumb not in current_branch:
                    current_branch[breadcrumb] = self._build_tree([*breadcrumbs], method)
                    break
                current_branch = current_branch[breadcrumb]
            else:
                if current_branch in ['GET', 'POST'] and current_branch != method:
                    raise DifferentMethodsException(uri, current_branch, method)
        return self.tree

    def _parse_uri(self, uri: str) -> Generator:
        """
        Генератор, разделяющий строку-URI на "хлебные крошки", игнорируя значения по нужным IgnoreRule правилам
        :param uri: исходная строка маршрута (URI)
        :return: ~ (crumb for crumb in uri.split('/'))
        """
        for crumb in uri.split('/'):
            for ignore_rule in self.IGNORE_LIST:
                if not ignore_rule.is_valid(crumb):
                    break
            else:
                yield crumb

    @staticmethod
    def _build_tree(breadcrumbs: List, method: str) -> dict:
        """
        Метод для построения продолжения ветки дерева.
        :param breadcrumbs: список крошек, которых нет в основном дереве
        :param method: Значение метода вызова handler (POST, GET, etc)
        :return: {crumb1: {crumb2: METHOD}}
        """
        current_obj = method
        for breadcrumb in reversed(breadcrumbs):
            current_obj = {breadcrumb: current_obj}
        return current_obj
