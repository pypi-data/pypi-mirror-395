pyscaffoldext-pre-commit-ruff
=============================

`PyScaffold`_ extension to use the `Ruff Linter`_ and `Ruff Formatter`_
in place of the `Pre Commit Extension`_, ``putup --pre-commit`` defaults
`flake8`_ and `isort`_.

The ``ruff`` configuration is added to ``pyproject.toml`` because
``ruff`` does not support ``setup.cfg``. Some `Ruff Linter`_ recommended
settings are commented out, for consistency with `PyScaffold`_'s
``flake8`` settings.

`Codespell`_ is added to `pre-commit`_ configuration in
``.pre-commit-config.yaml``; uncomment to enable.

`Mypy`_ settings are added to ``setup.cfg``.

Usage
-----

Just install this package with
``pip install pyscaffoldext-pre-commit-ruff`` and note that ``putup -h``
shows a new option ``--pre-commit-ruff``. Use this flag to use the `Ruff
Linter`_ and `Ruff Formatter`_ in place of ``putup --pre-commit``
defaults `flake8`_ and `isort`_.

.. _pyscaffold-notes:

Making Changes & Contributing
-----------------------------

This project uses `pre-commit`_, please make sure to install it before
making any changes:

::

   uv tool install pre-commit
   cd pyscaffoldext-pre-commit-ruff
   pre-commit install

It is a good idea to update the hooks to the latest version:

::

   pre-commit autoupdate

Note
----

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.

.. _PyScaffold: https://pyscaffold.org/
.. _Ruff Linter: https://docs.astral.sh/ruff/linter/
.. _Ruff Formatter: https://docs.astral.sh/ruff/formatter/
.. _Pre Commit Extension: https://pyscaffold.org/en/stable/features.html#pre-commit-hooks
.. _flake8: https://flake8.pycqa.org/
.. _isort: https://pycqa.github.io/isort/
.. _Codespell: https://github.com/codespell-project/codespell
.. _pre-commit: https://pre-commit.com/
.. _Mypy: https://mypy.readthedocs.io/
