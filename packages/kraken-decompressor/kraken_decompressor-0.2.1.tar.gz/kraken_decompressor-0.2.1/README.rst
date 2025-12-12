====================
kraken-decompressor
====================

.. start short_desc

**Oodle/Kraken decompressor.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/kraken-decompressor/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/kraken-decompressor/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/kraken-decompressor/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/kraken-decompressor/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/kraken-decompressor/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/kraken-decompressor/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/kraken-decompressor/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/kraken-decompressor/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/kraken-decompressor/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/kraken-decompressor/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/kraken-decompressor/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/kraken-decompressor?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/kraken-decompressor?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/kraken-decompressor
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/kraken-decompressor
	:target: https://pypi.org/project/kraken-decompressor/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/kraken-decompressor?logo=python&logoColor=white
	:target: https://pypi.org/project/kraken-decompressor/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/kraken-decompressor
	:target: https://pypi.org/project/kraken-decompressor/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/kraken-decompressor
	:target: https://pypi.org/project/kraken-decompressor/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/kraken-decompressor
	:target: https://github.com/domdfcoding/kraken-decompressor/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/kraken-decompressor
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/kraken-decompressor/v0.2.1
	:target: https://github.com/domdfcoding/kraken-decompressor/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/kraken-decompressor
	:target: https://github.com/domdfcoding/kraken-decompressor/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/kraken-decompressor
	:target: https://pypi.org/project/kraken-decompressor/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``kraken-decompressor`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install kraken-decompressor

.. end installation

Usage
--------------

``kraken-decompressor`` provides a single function, ``decompress``.

.. code-block:: python

	def decompress(src: bytes, dst_len) -> bytes: ...

The function takes two arguments, the compressed data ``src`` (as ``bytes``),
and the size of the decompressed data ``dst_len`` (as ``int``).
The function returns the decompressed data as ``bytes``.
