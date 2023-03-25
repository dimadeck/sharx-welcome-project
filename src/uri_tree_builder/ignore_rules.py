
class IgnoreRule:
    """
    Класс, используемый для определения валидности "хлебной крошки" в методе URITreeBuilder._parse_uri

    if IgnoreRule.is_valid(string):
        # correct crumb
        ...
    """
    @classmethod
    def is_valid(cls, crumb: str) -> bool:
        raise NotImplementedError


class WordIgnoreRule(IgnoreRule):
    WORD = None

    @classmethod
    def is_valid(cls, crumb: str) -> bool:
        if crumb != cls.WORD:
            return True


class APIWordIgnoreRule(WordIgnoreRule):
    WORD = 'api'


class V1WordIgnoreRule(WordIgnoreRule):
    WORD = 'v1'


class EmptyIgnoreRule(IgnoreRule):
    @classmethod
    def is_valid(cls, crumb: str) -> bool:
        return bool(crumb)


class CommandIgnoreRule(IgnoreRule):
    @classmethod
    def is_valid(cls, crumb: str) -> bool:
        return not (crumb.startswith('{') and crumb.endswith('}'))

