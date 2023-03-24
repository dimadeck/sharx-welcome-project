from uri_tree_builder.exceptions import DifferentMethodsException
from uri_tree_builder.uri_tree_builder import URITreeBuilder


def scenario_one(uri_tree_builder):
    input_list = [
        ("GET", "/api/v1/cluster/metrics"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")
    ]
    return uri_tree_builder.build_tree(input_list)


def scenario_two(uri_tree_builder):
    input_list = [
        ("GET", "/api/v1/cluster/freenodes/list"),
        ("GET", "/api/v1/cluster/nodes"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
        ("POST", "/api/v1/cluster/{cluster}/plugins")
    ]

    return uri_tree_builder.build_tree(input_list)


def scenario_with_exception(uri_tree_builder):
    input_list = [
        ("POST", "/api/v1/cluster/freenodes/list")
    ]
    try:
        uri_tree_builder.build_tree(input_list)
    except DifferentMethodsException as e:
        # URI: /api/v1/cluster/freenodes/list. Old('GET') and new(POST) methods are different
        print(e)
    return uri_tree_builder.tree


def main():
    uri_tree_builder = URITreeBuilder()

    scenario_one(uri_tree_builder)
    print(uri_tree_builder.tree)
    # {'cluster': {'metrics': 'GET', 'plugins': 'POST'}}

    scenario_two(uri_tree_builder)
    print(uri_tree_builder.tree)
    # {'cluster': {'metrics': 'GET', 'plugins': 'POST', 'freenodes': {'list': 'GET'}, 'nodes': 'GET'}}

    scenario_with_exception(uri_tree_builder)
    print(uri_tree_builder.tree)
    # {'cluster': {'metrics': 'GET', 'plugins': 'POST', 'freenodes': {'list': 'GET'}, 'nodes': 'GET'}}


if __name__ == '__main__':
    main()
