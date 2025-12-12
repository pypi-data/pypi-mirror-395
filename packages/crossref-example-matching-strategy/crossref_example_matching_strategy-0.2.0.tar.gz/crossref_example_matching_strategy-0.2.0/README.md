# Example Matching Strategy

This is meant to demonstrate how to create a strategy for use with the Crossref matching service (marple).

It uses [Poetry](https://python-poetry.org/) to manage dependencies and build the package.

`crossref-matcher` is a required dependency for development, it allows the import of the `Strategy` class in [`strategy.py`](src/crossref_example_matching_strategy/strategy.py). See [pyproject.toml](pyproject.toml).

The strategy can be loaded by the matching service after it is installed as a dependency there.
