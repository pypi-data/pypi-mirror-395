"""Add pre-commit-ruff extension."""

from argparse import ArgumentParser
from functools import partial, reduce
from typing import List

from pyscaffold import structure, toml
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension, include
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.operations import FileOp, no_overwrite
from pyscaffold.structure import (
    AbstractContent,
    Node,
    ResolvedLeaf,
    reify_leaf,
)
from pyscaffold.templates import get_template
from pyscaffold.update import ConfigUpdater

from . import templates as my_templates

PYPROJ_INSERT_AFTER = 'version_scheme = "no-guess-dev"\n'


class PreCommitRuff(Extension):
    """Generate pre-commit configuration file for Ruff (includes `--pre-commit`)."""

    def augment_cli(self, parser: ArgumentParser):
        """Augments the command-line interface parser.

        See :obj:`~pyscaffold.extension.Extension.augment_cli`.
        """
        parser.add_argument(
            self.flag,
            help=self.help_text,
            nargs=0,
            action=include(
                PreCommit(),
                self,
            ),
        )
        return self

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activates See :obj:`pyscaffold.extension.Extension.activate`.

        Args:
            actions (list): list of actions to perform

        Returns:
            list: updated list of actions
        """
        return self.register(
            actions,
            add_files,
            after="pyscaffold.extensions.pre_commit:add_files",
        )


def add_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Replace .pre-commit-config.yaml. Update setup.cfg and pyproject.toml.

    Add mypy section to setup.cfg.
    Remove flake8 section from setup.cfg. Ruff replaces flake8.

    Add ruff configuration to pyproject.toml.
    """
    files: Structure = {
        ".pre-commit-config.yaml": (
            get_template(
                name="pre-commit-ruff-config",
                relative_to=my_templates.__name__,
            ),
            no_overwrite(),
        ),
        "setup.cfg": modify_setupcfg(struct["setup.cfg"], opts),
    }

    struct = structure.modify(
        struct,
        "pyproject.toml",
        partial(modify_pyproject, opts),
    )
    return structure.merge(struct, files), opts


def modify_setupcfg(definition: Node, opts: ScaffoldOpts) -> ResolvedLeaf:
    """Modify setup.cfg to add template settings before it is written.

    See :obj:`pyscaffold.operations`.
    """
    content, action = reify_leaf(definition, opts)  # pyright: ignore [reportArgumentType]

    setupcfg = ConfigUpdater().read_string(str(content))

    modifiers = (add_setupcfg,)
    new_setupcfg = reduce(lambda acc, fn: fn(acc, opts), modifiers, setupcfg)

    return str(new_setupcfg), action


def add_setupcfg(setupcfg: ConfigUpdater, opts) -> ConfigUpdater:
    """Add section(s) to setup.cfg."""
    template = ConfigUpdater().read_string(
        str(
            structure.reify_content(
                get_template(
                    name="setup_cfg",
                    relative_to=my_templates.__name__,
                ),
                opts,
            ),
        )
    )

    setupcfg.remove_section("flake8")

    for k in template:
        setupcfg["pyscaffold"].add_before.section(k)
        setupcfg[k] = template[k].detach()
    setupcfg["pyscaffold"].add_before.space(newlines=1)

    return setupcfg


def modify_pyproject(
    opts: ScaffoldOpts, content: AbstractContent, file_op: FileOp
) -> ResolvedLeaf:
    """Add Ruff configuration to pyproject.toml."""
    pyproj_new = toml.loads(
        "\n".join(
            (
                str(structure.reify_content(content, opts)),
                str(structure.reify_content(my_templates.pyproject_toml, opts)),
            )
        )
    )
    return toml.dumps(pyproj_new), file_op
