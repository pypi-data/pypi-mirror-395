from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_wex_core.const.globals import COMMAND_TYPE_ADDON
from wexample_wex_core.decorator.command import command

if TYPE_CHECKING:
    from wexample_wex_core.context.execution_context import ExecutionContext


@command(type=COMMAND_TYPE_ADDON)
def test__run__all(context: ExecutionContext) -> None:
    import pytest

    from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager

    # Change to project root directory
    workdir = context.kernel.workdir.get_path()
    os.chdir(workdir)

    context.io.log(f"Starting pytest test suite from {workdir}")

    # TODO Finaliser le registre pour pouvoir lister les tests
    #  Voir /home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex/src/core/file/KernelRegistryFileStructure.py
    #  Voir /home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex/src/core/file/AbstractFileSystemStructure.py
    #  - Recopier un maximum de propriétés utiles dur genre on_missing ou atre
    #  - Créer KernelRegistryFileStructure basé sur YamlFile + KernelChild
    #  - Créer le registre comme avant et le sauver dans tmp.
    #  - Le registre identifier les fichier test pour chaque commande, qu'on réutilisera ici.
    # Build pytest arguments explicitly to avoid using sys.argv
    pytest_args = [
        "tests",  # Run tests from the tests directory
        "--color=yes",  # Enable colored output
        "-v",  # Verbose output
    ]

    # Add addons tests directories
    for addon in context.kernel.get_addons().values():
        assert isinstance(addon, AbstractAddonManager)
        context.io.log(f"Adding tests from addon: {addon.get_snake_short_class_name()}")
        pytest_args.append(addon.workdir.get_path().resolve() / "tests")

    context.io.log(f"Running pytest with args: {' '.join(pytest_args)}")

    # Run pytest with explicit arguments
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        context.io.success("All tests passed!")
    else:
        context.io.error(f"Tests failed with exit code: {exit_code}")
