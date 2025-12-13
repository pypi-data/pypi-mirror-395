from mypy.plugin import Plugin  # type: ignore[import-untyped]


class PyJSXPlugin(Plugin):
    import pyjsx.auto_setup  # type: ignore[import-unused]


def plugin(_version: str) -> type[Plugin]:
    return PyJSXPlugin
