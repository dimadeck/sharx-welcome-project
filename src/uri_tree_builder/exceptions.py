class DifferentMethodsException(Exception):
    def __init__(self, uri, old_value, new_value):
        super().__init__(f"URI: {uri}. Old('{old_value}') and new({new_value}) methods are different")
