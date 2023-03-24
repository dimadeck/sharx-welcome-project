import pytest
from uri_tree_builder.uri_tree_builder import URITreeBuilder


@pytest.fixture(scope='module')
def uri_tree_builder():
    return URITreeBuilder()
