from typing import List

from uri_tree_builder.exceptions import DifferentMethodsException
from uri_tree_builder.ignore_rules import APIWordIgnoreRule, V1WordIgnoreRule, CommandIgnoreRule, EmptyIgnoreRule


class URITreeBuilder:
    IGNORE_LIST = [APIWordIgnoreRule, V1WordIgnoreRule, CommandIgnoreRule, EmptyIgnoreRule]

    def __init__(self):
        self._tree = {}

    @property
    def tree(self) -> dict:
        return self._tree

    def build_tree(self, input_list: List) -> dict:
        for method, uri in input_list:
            breadcrumbs = self._parse_uri(uri)
            current_branch = self._tree
            for breadcrumb in breadcrumbs:
                if breadcrumb not in current_branch:
                    current_branch[breadcrumb] = self._build_tree([*breadcrumbs], method)
                    continue
                current_branch = current_branch[breadcrumb]
            else:
                if current_branch in ['GET', 'POST'] and current_branch != method:
                    raise DifferentMethodsException(uri, current_branch, method)
        return self.tree

    def _parse_uri(self, uri: str):
        for crumb in uri.split('/'):
            for ignore_rule in self.IGNORE_LIST:
                if not ignore_rule.is_valid(crumb):
                    break
            else:
                yield crumb

    @staticmethod
    def _build_tree(breadcrumbs: List, method: str) -> dict:
        current_obj = method
        for breadcrumb in reversed(breadcrumbs):
            current_obj = {breadcrumb: current_obj}
        return current_obj
