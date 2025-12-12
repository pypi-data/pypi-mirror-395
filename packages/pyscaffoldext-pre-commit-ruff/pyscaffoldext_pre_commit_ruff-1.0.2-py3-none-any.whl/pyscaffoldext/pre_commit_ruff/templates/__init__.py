"""Location for pre-commit-ruff templates."""

import string

from pyscaffold import toml
from pyscaffold.actions import ScaffoldOpts
from pyscaffold.templates import get_template


def pyproject_toml(opts: ScaffoldOpts) -> str:
    """Load and substitute template."""
    template: string.Template = get_template(
        name="pyproject_toml",
        relative_to=__name__,
    )
    config = toml.loads(template.safe_substitute(opts))
    return toml.dumps(config)
