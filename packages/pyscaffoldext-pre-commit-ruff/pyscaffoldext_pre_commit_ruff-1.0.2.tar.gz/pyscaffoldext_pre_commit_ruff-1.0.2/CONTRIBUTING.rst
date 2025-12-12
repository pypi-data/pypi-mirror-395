Contributing
============

Welcome to ``pyscaffoldext-pre-commit-ruff`` contributor’s guide.

This document focuses on getting any potential contributor familiarized
with the development processes, but `other kinds of contributions`_ are
also appreciated.

If you are new to using `git`_ or have never collaborated in a project
previously, please have a look at `contribution-guide.org`_. Other
resources are also listed in the excellent `guide created by
FreeCodeCamp`_  [1]_.

Please notice, all users and contributors are expected to be **open,
considerate, reasonable, and respectful**. When in doubt, `Python
Software Foundation’s Code of Conduct`_ is a good reference in terms of
behavior guidelines.

Please follow `pyscaffold’s contributor’s guide`_.

Issue Reports
-------------

If you experience bugs or general issues with
``pyscaffoldext-pre-commit-ruff``, please have a look on the `issue
tracker`_. If you don’t see anything useful there, please feel free to
fire an issue report.

.. container:: {tip}

   Please don’t forget to include the closed issues in your search.
   Sometimes a solution was already reported, and the problem is
   considered **solved**.

New issue reports should include information about your programming
environment (e.g., operating system, Python version) and steps to
reproduce the problem. Please try also to simplify the reproduction
steps to a very minimal example that still illustrates the problem you
are facing. By removing other factors, you help us to identify the root
cause of the issue.

Documentation Improvements
--------------------------

You can help improve ``pyscaffoldext-pre-commit-ruff`` docs by making
them more readable and coherent, or by adding missing information and
correcting mistakes.

``pyscaffoldext-pre-commit-ruff`` documentation uses `Sphinx`_ as its
main documentation compiler. This means that the docs are kept in the
same repository as the project code, and that any documentation update
is done in the same way was a code contribution—i.e.,
`reStructuredText`_.

.. container:: {tip}

   Please notice that the `GitHub web interface`_ provides a quick way
   of propose changes in ``pyscaffoldext-pre-commit-ruff``\ ’s files.
   While this mechanism can be tricky for normal code contributions, it
   works perfectly fine for contributing to the docs, and can be quite
   handy.

   If you are interested in trying this method out, please navigate to
   the ``docs`` folder in the source `repository`_, find which file you
   would like to propose changes and click in the little pencil icon at
   the top, to open `GitHub’s code editor`_. Once you finish editing the
   file, please write a message in the form at the bottom of the page
   describing which changes have you made and what are the motivations
   behind them and submit your proposal.

When working on documentation changes in your local machine, you can
compile them using `tox`_ :

.. code:: bash

   tox -e docs

and use Python’s built-in web server for a preview in your web browser
(``http://localhost:8000``):

.. code:: bash

   python3 -m http.server --directory 'docs/_build/html'

Code Contributions
------------------

The architecture follows `Extending PyScaffold`_.

Submit an issue
~~~~~~~~~~~~~~~

Before you work on any non-trivial code contribution it’s best to first
create a report in the `issue tracker`_ to start a discussion on the
subject. This often provides additional considerations and avoids
unnecessary work.

Create an environment
~~~~~~~~~~~~~~~~~~~~~

Before you start coding, we recommend creating an isolated `virtual
environment`_ to avoid any problems with your installed Python packages.
This can easily be done via either `uv`_:

::

   uv tool install tox --with tox-uv
   uv venv <PATH TO VENV>
   source <PATH TO VENV>/bin/activate

or `Miniconda`_:

::

   conda create -n pyscaffoldext-pre-commit-ruff python=3 six virtualenv pytest pytest-cov
   conda activate pyscaffoldext-pre-commit-ruff

Clone the repository
~~~~~~~~~~~~~~~~~~~~

1. Create an user account on GitHub if you do not already have one.

2. Fork the project `repository`_: click on the *Fork* button near the
   top of the page. This creates a copy of the code under your account
   on GitHub.

3. Clone this copy to your local disk:

   ::

      git clone git@github.com:YourLogin/pyscaffoldext-pre-commit-ruff.git
      cd pyscaffoldext-pre-commit-ruff

4. You should run:

   ::

      uv pip install -U setuptools -e .

   to be able to import the package under development in the Python
   REPL.

5. Install `pre-commit`_:

   .. code:: bash

      uv tool install pre-commit
      pre-commit install

   ``pyscaffoldext-pre-commit-ruff`` comes with a lot of hooks
   configured to automatically help the developer to check the code
   being written.

Implement your changes
~~~~~~~~~~~~~~~~~~~~~~

1. Create a branch to hold your changes:

   .. code:: bash

      git checkout -b my-feature

   and start making changes. Never work on the main branch!

2. Start your work on this branch. Don’t forget to add `docstrings`_ to
   new functions, modules and classes, especially if they are part of
   public APIs.

3. Add yourself to the list of contributors in ``AUTHORS.rst``.

4. When you’re done editing, do:

   .. code:: bash

      git add <MODIFIED FILES>
      git commit

   to record your changes in `git`_.

   Please make sure to see the validation messages from `pre-commit`_
   and fix any eventual issues. This should automatically use `ruff`_ to
   check/fix the code style in a way that is compatible with the
   project.

   .. container:: {important}

      Don’t forget to add unit tests and documentation in case your
      contribution adds an additional feature and is not just a bugfix.

      Moreover, writing a `descriptive commit message`_ is highly
      recommended. In case of doubt, you can check the commit history
      with:

      .. code:: bash

         git log --graph --decorate --pretty=oneline --abbrev-commit --all

      to look for recurring communication patterns.

5. Please check that your changes don’t break any unit tests with:

   ::

      tox

   (after having installed `tox`_ with
   ``uv tool install tox --with tox-uv`` or ``pipx``).

   You can also use `tox`_ to run several other pre-configured tasks in
   the repository. Try ``tox -av`` to see a list of the available
   checks.

Submit your contribution
~~~~~~~~~~~~~~~~~~~~~~~~

1. If everything works fine, push your local branch to the remote server
   with:

   .. code:: bash

      git push -u origin my-feature

2. Go to the web page of your fork and click “Create pull request” to
   send your changes for review.

   Find more detailed information in `creating a PR`_. You might also
   want to open the PR as a draft first and mark it as ready for review
   after the feedbacks from the continuous integration (CI) system or
   any required fixes.

Troubleshooting
~~~~~~~~~~~~~~~

The following tips can be used when facing problems to build or test the
package:

1. Make sure to fetch all the tags from the upstream `repository`_. The
   command ``git describe --abbrev=0 --tags`` should return the version
   you are expecting. If you are trying to run CI scripts in a fork
   repository, make sure to push all the tags. You can also try to
   remove all the egg files or the complete egg folder, i.e., ``.eggs``,
   as well as the ``*.egg-info`` folders in the ``src`` folder or
   potentially in the root of your project.

2. Sometimes `tox`_ misses out when new dependencies are added,
   especially to ``setup.cfg`` and ``docs/requirements.txt``. If you
   find any problems with missing dependencies when running a command
   with `tox`_, try to recreate the ``tox`` environment using the ``-r``
   flag. For example, instead of:

   .. code:: bash

      tox -e docs

   Try running:

   .. code:: bash

      tox -r -e docs

3. Make sure to have a reliable `tox`_ installation that uses the
   correct Python version (e.g., 3.7+). When in doubt you can run:

   .. code:: bash

      tox --version
      # OR
      which tox

   If you have trouble and are seeing weird errors upon running `tox`_,
   you can also try to create a dedicated `virtual environment`_ with a
   `tox`_ binary freshly installed. For example:

   .. code:: bash

      uv venv .venv
      source .venv/bin/activate
      .venv/bin/pip install tox
      .venv/bin/tox -e all

4. `Pytest can drop you`_ in an interactive session in the case an error
   occurs. In order to do that you need to pass a ``--pdb`` option (for
   example by running ``tox -- -k <NAME OF THE FALLING TEST> --pdb``).
   You can also setup breakpoints manually instead of using the
   ``--pdb`` option.

Maintainer tasks
----------------

Releases
~~~~~~~~

If you are part of the group of maintainers and have correct user
permissions on `PyPI`_, the following steps can be used to release a new
version for ``pyscaffoldext-pre-commit-ruff``:

1. Make sure all unit tests are successful.
2. Tag the current commit on the main branch with a release tag, e.g.,
   ``v1.2.3``.
3. Push the new tag to the upstream `repository`_, e.g.,
   ``git push upstream v1.2.3``
4. Clean up the ``dist`` and ``build`` folders with ``tox -e clean`` (or
   ``rm -rf dist build``) to avoid confusion with old builds and Sphinx
   docs.
5. Run ``tox -e build`` and check that the files in ``dist`` have the
   correct version (no ``.dirty`` or `git`_ hash) according to the
   `git`_ tag. Also check the sizes of the distributions, if they are
   too big (e.g., > 500KB), unwanted clutter may have been accidentally
   included.

.. [1]
   Even though, these resources focus on open source projects and
   communities, the general ideas behind collaborating with other
   developers to collectively create software are general and can be
   applied to all sorts of environments, including private companies and
   proprietary code bases.

.. _other kinds of contributions: https://opensource.guide/how-to-contribute
.. _git: https://git-scm.com
.. _contribution-guide.org: https://www.contribution-guide.org/
.. _guide created by FreeCodeCamp: https://github.com/freecodecamp/how-to-contribute-to-open-source
.. _Python Software Foundation’s Code of Conduct: https://www.python.org/psf/conduct/
.. _pyscaffold’s contributor’s guide: https://pyscaffold.org/en/stable/contributing.html
.. _issue tracker: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff/issues
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/
.. _GitHub web interface: https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
.. _repository: https://github.com/jfishe/pyscaffoldext-pre-commit-ruff
.. _GitHub’s code editor:  https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
.. _tox: https://tox.readthedocs.io/en/stable/
.. _Extending PyScaffold: https://pyscaffold.org/en/stable/extensions.html#extending-pyscaffold
.. _virtual environment: https://realpython.com/python-virtual-environments-a-primer/
.. _uv: https://docs.astral.sh/uv/
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _pre-commit: https://pre-commit.com/
.. _docstrings: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
.. _ruff: https://docs.astral.sh/ruff
.. _descriptive commit message: https://cbea.ms/git-commit/
.. _creating a PR: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
.. _Pytest can drop you: https://docs.pytest.org/en/stable/how-to/failures.html#using-python-library-pdb-with-pytest
.. _PyPI: https://pypi.org/
