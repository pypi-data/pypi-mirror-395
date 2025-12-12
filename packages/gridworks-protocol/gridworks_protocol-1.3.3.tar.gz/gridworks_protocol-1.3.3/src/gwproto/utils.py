import re

snake_add_underscore_to_camel_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(name: str) -> str:
    return snake_add_underscore_to_camel_pattern.sub("_", name).lower()


def snake_to_camel(word: str) -> str:
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def rld_alias(alias: str) -> str:
    return ".".join(reversed(alias.split(".")))
