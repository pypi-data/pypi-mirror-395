from pathlib import Path

import pytest

from sphinx_ape._utils import extract_package_name, extract_source_url


@pytest.fixture(scope="session")
def create_setup_py():
    def fn(
        base_path: Path, name: str = "ape-myplugin", url: bool = False, source_url: bool = False
    ):
        content = f"""
#!/usr/bin/env python

from setuptools import find_packages, setup
extras_require = {{
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0",  # Core testing package
    ],
}}
setup(
    name="{name}",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.12",
    ],
"""
        if url:
            content = f'{content}\n  url="https://github.com/ApeWorX/{name}",'
        if source_url:
            content = (
                f"{content}    project_urls={{\n        "
                f'"Source": "https://github.com/ApeWorX/{name}",\n    }},'
            )

        content = f"{content}\n)"
        path = base_path / "setup.py"
        path.write_text(content)
        return path

    return fn


def test_extract_package_name_setup_py(temp_path, create_setup_py):
    name = "ape-myplugin"
    create_setup_py(temp_path, name)
    actual = extract_package_name(temp_path)
    assert actual == name


def test_extract_source_url_from_setup_py_project_urls_source(temp_path, create_setup_py):
    name = "ape-myplugin"
    create_setup_py(temp_path, name, source_url=True)
    actual = extract_source_url(temp_path)
    expected = f"https://github.com/ApeWorX/{name}"
    assert actual == expected


def test_extract_source_url_from_setup_py_url(temp_path, create_setup_py):
    name = "ape-myplugin"
    create_setup_py(temp_path, name, url=True)
    actual = extract_source_url(temp_path)
    expected = f"https://github.com/ApeWorX/{name}"
    assert actual == expected
