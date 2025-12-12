import re
from typing import Any, Dict, List, Tuple, Type, Union, cast

from detect_secrets.filters.heuristic import is_not_alphanumeric_string, is_sequential_string, is_templated_secret
from detect_secrets.plugins.base import BasePlugin, RegexBasedDetector
from detect_secrets.plugins.keyword import DENYLIST
from pydantic import BaseModel
from ruamel.yaml.comments import TaggedScalar
from ruamel.yaml.scalarint import BinaryInt, HexCapsInt, HexInt, OctalInt


def get_all_regex_plugins() -> List[BasePlugin]:
    from detect_secrets.core.plugins.util import get_mapping_from_secret_type_to_class

    defintions: List[Type[BasePlugin]] = list(get_mapping_from_secret_type_to_class().values())
    implementations = [x() for x in defintions]
    return implementations


ALL_REGEX_PLUGINS = [x for x in get_all_regex_plugins() if isinstance(x, RegexBasedDetector)]
KEYWORD_REGEXES = [re.compile(x, re.IGNORECASE) for x in DENYLIST]

# Addded [^{] at the end to avoid matching jinja templates
KEYWORD_IN_VALUES_REGEXES = [re.compile(x + r"[^\s]*\s*[=:]\s*[^{]", re.IGNORECASE) for x in DENYLIST]


def is_secret_key(keyword: str) -> bool:
    return any(x.search(keyword) for x in KEYWORD_REGEXES)


def is_jinja_or_object(value: str) -> bool:
    if not isinstance(value, str):
        return True

    # filtering sequential strings, e.g. "aaaaaa", "123456"
    if is_sequential_string(value):
        return True

    # filtering if starts with not AN
    # part of FOLLOWED_BY_COLON_REGEX
    if not value[0].isalnum():
        return True

    # Jinja may reference variables, that sound like secret
    return "{{" in value


def filter_secret(keyword: str) -> bool:
    # filtering IP addresses
    if is_not_alphanumeric_string(keyword):
        return True
    # filtering secrets in jinja templates
    return is_templated_secret(keyword)


def is_secret_value(value: str) -> bool:
    if not isinstance(value, str):
        return False

    regex_candidates = [x.search(value) for x in KEYWORD_IN_VALUES_REGEXES]
    if any(not filter_secret(x.group(0)) for x in regex_candidates if x is not None):
        return True

    plugin_candidates = [x.analyze_string(value) for x in ALL_REGEX_PLUGINS]
    result = any(not filter_secret(x) for plugin in plugin_candidates for x in plugin)
    return result


class ScalarBool:
    def __init__(self, bool_value: bool, original_value: str) -> None:
        self.bool_value = bool_value
        self.original_value = original_value

    def __str__(self) -> str:
        return str(self.bool_value)


class ScalarBoolYes(ScalarBool):
    pass


class ScalarBoolNo(ScalarBool):
    pass


class ScalarBoolfactory:
    @staticmethod
    def from_string(value: Any, parsed_value: bool) -> Union[ScalarBool, bool]:
        if value in ["True", "yes", "y", "On", "on"]:
            return ScalarBoolYes(parsed_value, value)
        if value in ["False", "no", "n", "Off", "off"]:
            return ScalarBoolNo(parsed_value, value)
        return parsed_value


class ScalarTimestamp:
    def __init__(self, str_value: str) -> None:
        self.str_value = str_value


class SpotterObfuscated(BaseModel):
    """Class where we save metadata about which fields were obfuscated."""

    type: str
    path: List[Union[int, str]]

    def to_parent(self, path_item: Union[int, str]) -> "SpotterObfuscated":
        """
        Create new object which contains also parent path.

        :param path_item: Path that needs to be inserted at the beginning
        :return: SpotterObfuscated with added parent path
        """
        temp = cast(List[Union[int, str]], [path_item])
        return SpotterObfuscated(type=self.type, path=temp + self.path)


ObfuscatedInput = List[SpotterObfuscated]


def remove_secret_parameter_values(  # noqa: PLR0911,PLR0912
    yaml_key: Any, skip_detect_secrets: bool
) -> Tuple[Any, ObfuscatedInput]:
    """
    Remove secret parameter values from YAML.

    :param yaml_key: YAML key
    :param secret_values: List of detected secret values
    :return: Updated YAML key
    """
    ## cleanup data, so we can put it into json
    if isinstance(yaml_key, BinaryInt):
        return yaml_key, [SpotterObfuscated(type="BinaryInt", path=[])]
    if isinstance(yaml_key, OctalInt):
        return yaml_key, [SpotterObfuscated(type="OctalInt", path=[])]
    if isinstance(yaml_key, HexInt):
        return yaml_key, [SpotterObfuscated(type="HexInt", path=[])]
    if isinstance(yaml_key, HexCapsInt):
        return yaml_key, [SpotterObfuscated(type="HexCapsInt", path=[])]

    if isinstance(yaml_key, ScalarTimestamp):
        return yaml_key.str_value, [SpotterObfuscated(type="Timestamp", path=[])]

    if isinstance(yaml_key, ScalarBool):
        return yaml_key.bool_value, [SpotterObfuscated(type=yaml_key.__class__.__name__, path=[])]

    if isinstance(yaml_key, TaggedScalar):  # key: !!str '{sdgsgfdhfd}'
        return yaml_key.value, []

    if isinstance(yaml_key, bytes):  # key: !!binary | Base64....
        return None, [SpotterObfuscated(type="bytes", path=[])]

    if isinstance(yaml_key, str) and "\x00" in yaml_key:
        return yaml_key.replace("\x00", "\\u0000"), [SpotterObfuscated(type="EOF", path=[])]

    ## from here one we detect secrets
    if skip_detect_secrets:
        return yaml_key, []

    if isinstance(yaml_key, dict):
        return _remove_secret_parameter_from_dict(yaml_key)

    if isinstance(yaml_key, list):
        return _remove_secret_parameter_from_list(yaml_key)

    if isinstance(yaml_key, str) and is_secret_value(yaml_key):
        return None, [SpotterObfuscated(type="str", path=[])]

    return yaml_key, []


def _remove_secret_parameter_from_dict(data: Dict[str, Any]) -> Tuple[Any, ObfuscatedInput]:
    obfuscated: ObfuscatedInput = []
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(key, str) and is_secret_key(key) and not is_jinja_or_object(value):
            obfuscated.append(SpotterObfuscated(type="str", path=[key]))
            result[key] = None
            continue
        cleaned, items = remove_secret_parameter_values(value, False)
        result[key] = cleaned
        obfuscated.extend(item.to_parent(key) for item in items)
    return result, obfuscated


def _remove_secret_parameter_from_list(data: List[Any]) -> Tuple[Any, ObfuscatedInput]:
    obfuscated: ObfuscatedInput = []
    result = []
    for key, value in enumerate(data):
        cleaned, items = remove_secret_parameter_values(value, False)
        result.append(cleaned)
        obfuscated.extend(item.to_parent(key) for item in items)
    return result, obfuscated
