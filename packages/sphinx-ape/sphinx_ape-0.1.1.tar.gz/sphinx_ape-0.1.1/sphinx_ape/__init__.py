def __getattr__(name: str):
    if name == "setup":
        from sphinx_ape.sphinx_ext.plugin import setup

        return setup

    else:
        raise AttributeError(name)


__all__ = [
    "setup",
]
