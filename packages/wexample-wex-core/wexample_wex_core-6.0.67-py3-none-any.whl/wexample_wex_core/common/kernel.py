from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_app.common.abstract_kernel import AbstractKernel
from wexample_app.common.mixins.command_line_kernel import CommandLineKernel
from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel
from wexample_app.const.output import OUTPUT_FORMAT_STR, OUTPUT_TARGET_NONE
from wexample_app.output.app_none_output_handler import AppNoneOutputHandler
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_app.command.option import Option
    from wexample_app.const.types import CommandLineArgumentsList
    from wexample_app.output.abstract_app_output_handler import AbstractAppOutputHandler
    from wexample_app.resolver.abstract_command_resolver import AbstractCommandResolver
    from wexample_app.runner.abstract_command_runner import AbstractCommandRunner
    from wexample_config.const.types import DictConfig
    from wexample_filestate.utils.file_state_manager import FileStateManager
    from wexample_prompt.common.io_manager import IoManager

    from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager
    from wexample_wex_core.common.command_request import CommandRequest
    from wexample_wex_core.registry.kernel_registry import KernelRegistry
    from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir


@base_class
class Kernel(CommandRunnerKernel, CommandLineKernel, AbstractKernel):
    _config_arg_force_request_id: str | None = private_field(
        default=None,
        description="When request comes from another external process",
    )
    _config_arg_indentation_level: int | None = private_field(
        default=None,
        description="Prompt messages indentation level",
    )
    _config_arg_output_format: None | list[str] = private_field(
        default=None,
        description="Verbosity level of every logs",
    )
    _config_arg_output_target: None | list[str] = private_field(
        default=None,
        description="A target where to place the output",
    )
    _config_arg_quiet: bool = private_field(
        default=False,
        description="Disable verbosity, every log or message, useful to capture structured output",
    )
    _config_arg_v: bool = private_field(
        default=False,
        description="Default verbosity",
    )
    _config_arg_vv: bool = private_field(
        default=False,
        description="High verbosity",
    )
    _config_arg_vvv: bool = private_field(
        default=False,
        description="Maximum verbosity",
    )
    _registry: KernelRegistry = private_field(description="The configuration registry")

    def create_output_handlers(self) -> [AbstractAppOutputHandler]:
        """Initialize output handlers based on _config_arg_output_target.

        Replaces default stdout handler with handlers from registry according to output targets.
        """
        available_handlers = self._get_available_output_handlers()
        # Clear default handlers and add specified ones
        outputs = []

        for target in self._config_arg_output_target:
            if target in available_handlers:
                handler_class = available_handlers[target]
                outputs.append(handler_class(kernel=self))

        return outputs

    def get_addons(self) -> dict[str, AbstractAddonManager]:
        from wexample_wex_core.const.registries import REGISTRY_KERNEL_ADDON

        return self.get_registry(REGISTRY_KERNEL_ADDON).get_all()

    def get_configuration_registry(self) -> KernelRegistry:
        return self._registry

    def setup(
        self, addons: list[type[AbstractAddonManager]] | None = None
    ) -> AbstractKernel:
        response = super().setup()

        self._init_command_line_kernel()
        self._init_addons(addons=addons)
        self._init_resolvers()
        self._init_runners()
        self._init_middlewares()
        self._init_registry()

        return response

    def _build_single_command_request_from_arguments(
        self, arguments: CommandLineArgumentsList
    ):
        # Core command request takes a request id.
        return [
            self._get_command_request_class()(
                kernel=self,
                request_id=self._config_arg_force_request_id or arguments[0],
                name=arguments[1],
                arguments=arguments[2:],
                output_target=self._config_arg_output_target,
                output_format=self._config_arg_output_format,
            )
        ]

    def _create_workdir_state_manager(
        self,
        entrypoint_path: str,
        io: IoManager,
        config: DictConfig | None = None,
    ) -> FileStateManager:
        return self._get_workdir_state_manager_class().create_from_kernel(
            kernel=self, config=config or {}, io=io
        )

    def _get_available_output_handlers(self):
        """Get available output handlers for core kernel.

        Returns:
            Dictionary with stdout and file handlers
        """
        from wexample_app.const.output import OUTPUT_TARGET_FILE, OUTPUT_TARGET_STDOUT
        from wexample_app.output.app_stdout_output_handler import (
            AppStdoutOutputHandler,
        )

        from wexample_wex_core.output.request_file_output_handler import (
            RequestFileOutputHandler,
        )

        return {
            OUTPUT_TARGET_NONE: AppNoneOutputHandler,
            OUTPUT_TARGET_STDOUT: AppStdoutOutputHandler,
            OUTPUT_TARGET_FILE: RequestFileOutputHandler,
        }

    def _get_command_request_class(self) -> type[CommandRequest]:
        from wexample_wex_core.common.command_request import CommandRequest

        return CommandRequest

    def _get_command_resolvers(self) -> list[type[AbstractCommandResolver]]:
        from wexample_wex_core.resolver.addon_command_resolver import (
            AddonCommandResolver,
        )
        from wexample_wex_core.resolver.service_command_resolver import (
            ServiceCommandResolver,
        )

        return [
            # filestate: python-iterable-sort
            AddonCommandResolver,
            ServiceCommandResolver,
        ]

    def _get_command_runners(self) -> list[type[AbstractCommandRunner]]:
        from wexample_wex_core.runner.core_python_command_runner import (
            CorePythonCommandRunner,
        )
        from wexample_wex_core.runner.core_yaml_command_runner import (
            CoreYamlCommandRunner,
        )

        return [
            # Default runner.
            # filestate: python-iterable-sort
            CorePythonCommandRunner,
            CoreYamlCommandRunner,
        ]

    def _get_core_args(self) -> list[Option]:
        from wexample_app.command.option import Option
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        return super()._get_core_args() + [
            Option(
                name="quiet",
                is_flag=True,
                type=bool,
                value=VerbosityLevel.QUIET,
                description="Silence all output",
            ),
            Option(
                name="v",
                short_name="v",
                is_flag=True,
                type=bool,
                value=VerbosityLevel.MEDIUM,
                description="Medium verbosity",
            ),
            Option(
                name="vv",
                short_name="vv",
                is_flag=True,
                type=bool,
                value=VerbosityLevel.HIGH,
                description="High verbosity",
            ),
            Option(
                name="vvv",
                short_name="vvv",
                is_flag=True,
                type=bool,
                value=VerbosityLevel.MAXIMUM,
                description="Maximum verbosity",
            ),
            Option(
                name="output_format",
                type=str,
                value="str",
                description="The way to render the output",
            ),
            Option(
                name="output_target",
                type=str,
                value="str",
                description="The emplacement where placing the output (stdout, file, ...)",
                multiple=True,
                always_list=True,
            ),
            Option(
                name="indentation_level",
                is_flag=False,
                type=int,
                description="Number of indentation levels to use",
            ),
            Option(
                name="force_request_id",
                short_name="force_request_id",
                type=str,
                description="When an external process launches the request",
            ),
        ]

    def _get_workdir_state_manager_class(self) -> type[KernelWorkdir]:
        from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir

        return KernelWorkdir

    def _init_addons(
        self, addons: list[type[AbstractAddonManager]] | None = None
    ) -> None:
        from wexample_app.service.service_registry import ServiceRegistry

        from wexample_wex_core.const.registries import REGISTRY_KERNEL_ADDON

        cast(ServiceRegistry, self.set_registry(REGISTRY_KERNEL_ADDON))
        registry = self.register_items(REGISTRY_KERNEL_ADDON, addons or [])
        registry.instantiate_all(kernel=self)

    def _init_command_line_core_args(self) -> None:
        from wexample_helpers.helpers.array import array_unique

        super()._init_command_line_core_args()

        self._config_arg_output_format = (
            self._config_arg_output_format or OUTPUT_FORMAT_STR
        )
        # By default, the kernel does not return data, but only display io messages.
        # The output should be explicitly asked to be returned in file or output.
        self._config_arg_output_target = array_unique(
            self._config_arg_output_target or [OUTPUT_TARGET_NONE]
        )

    def _init_command_line_kernel(self: AbstractKernel) -> None:
        super()._init_command_line_kernel()
        # We can then use config.
        if self._config_arg_quiet:
            self.io.default_context_verbosity = VerbosityLevel.QUIET
            self.io.default_response_verbosity = VerbosityLevel.QUIET
        elif self._config_arg_v:
            self.io.default_context_verbosity = VerbosityLevel.DEFAULT
            self.io.default_response_verbosity = VerbosityLevel.DEFAULT
        elif self._config_arg_vv:
            self.io.default_context_verbosity = VerbosityLevel.HIGH
            self.io.default_response_verbosity = VerbosityLevel.HIGH
        elif self._config_arg_vvv:
            self.io.default_context_verbosity = VerbosityLevel.MAXIMUM
            self.io.default_response_verbosity = VerbosityLevel.MAXIMUM

        self.io.indentation = min(
            self._config_arg_indentation_level or self.io.indentation,
            int(self.io.terminal_width / 3),
        )

    def _init_middlewares(self) -> None:
        from wexample_wex_core.common.abstract_addon_manager import AbstractAddonManager

        classes = []
        for addon in self.get_addons().values():
            classes.extend(cast(AbstractAddonManager, addon).get_middlewares_classes())

        self.register_items("middlewares", classes)

    def _init_registry(self) -> None:
        from wexample_wex_core.path.kernel_registry_file import KernelRegistryFile
        from wexample_wex_core.workdir.kernel_workdir import KernelWorkdir

        kernel_registry_file = self.workdir.get_shortcut(
            KernelWorkdir.SHORTCUT_REGISTRY
        )
        assert isinstance(kernel_registry_file, KernelRegistryFile)

        # Registry has zero length.
        if kernel_registry_file.get_local_file().is_empty():
            # Create registry and dump in file
            self._registry = kernel_registry_file.create_registry_and_save(kernel=self)
        else:
            # Fill registry from existing file
            self._registry = kernel_registry_file.create_registry_from_content(
                kernel=self
            )
