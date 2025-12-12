from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from wexample_app.common.command import Command
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_app.common.command_request import CommandRequest

    from wexample_wex_core.common.command_method_wrapper import CommandMethodWrapper
    from wexample_wex_core.const.types import ParsedArgs
    from wexample_wex_core.context.execution_context import ExecutionContext


@base_class
class ExtendedCommand(Command):
    command_wrapper: CommandMethodWrapper = public_field(
        description="The wrapper holding the command function"
    )

    def __attrs_post_init__(self) -> None:
        # Now override function based on command_wrapper
        self.function = self.command_wrapper.function

    def execute_request(self, request: CommandRequest) -> Any:
        from wexample_app.helpers.response import response_normalize
        from wexample_app.response.failure_response import FailureResponse
        from wexample_app.response.multiple_response import MultipleResponse

        from wexample_wex_core.const.middleware import (
            MIDDLEWARE_OPTION_VALUE_ALLWAYS,
            MIDDLEWARE_OPTION_VALUE_OPTIONAL,
        )

        middlewares_attributes = self.command_wrapper.middlewares_attributes
        middlewares_registry = self.kernel.get_registry("middlewares")

        for name in middlewares_attributes:
            middleware_class = middlewares_registry.get_class(name)
            middleware = middleware_class(**middlewares_attributes[name])
            self.command_wrapper.set_middleware(middleware)

        function_kwargs = self._build_function_kwargs(request=request)

        if len(self.command_wrapper.middlewares) > 0:
            output = MultipleResponse(kernel=self.kernel)

            for middleware in self.command_wrapper.middlewares:
                show_progress = (
                    middleware.show_progress == MIDDLEWARE_OPTION_VALUE_ALLWAYS
                    or (
                        middleware.show_progress == MIDDLEWARE_OPTION_VALUE_OPTIONAL
                        and function_kwargs["show_progress"]
                    )
                )

                # Each middleware can multiply the executions,
                # e.g. executing the command on every file of a list.
                execution_contexts = middleware.build_execution_contexts(
                    command_wrapper=self.command_wrapper,
                    request=request,
                    function_kwargs=function_kwargs,
                )

                # Apply limit if specified
                if (
                    isinstance(middleware.max_iterations, int)
                    and middleware.max_iterations > 0
                ):
                    execution_contexts = execution_contexts[: middleware.max_iterations]
                    self.kernel.io.info(
                        f'Middleware "{middleware.get_short_class_name()}" truncated list to {middleware.max_iterations} items'
                    )

                # Check if middleware should run in parallel
                if middleware.parallel == MIDDLEWARE_OPTION_VALUE_ALLWAYS or (
                    middleware.parallel == MIDDLEWARE_OPTION_VALUE_OPTIONAL
                    and "parallel" in function_kwargs
                    and function_kwargs["parallel"]
                ):
                    # Execute passes in parallel using asyncio
                    responses = asyncio.run(
                        self._execute_passes_parallel(
                            execution_contexts=execution_contexts,
                        )
                    )

                    # Add all responses to output
                    for response in responses:
                        output.append(response)

                        # Check if we should stop on failure
                        if (
                            isinstance(response, FailureResponse)
                            and middleware.stop_on_failure
                        ):
                            # "Stop" does not mean "fail", so we just stop the process.
                            return output
                else:
                    i = 0
                    length = len(execution_contexts)

                    if show_progress:
                        # First bar.
                        request.kernel.io.progress(length, i)

                    # Execute passes sequentially
                    for context in execution_contexts:
                        # Use context.function if provided, otherwise use command's function
                        function_to_execute = context.function or self.function

                        response = response_normalize(
                            kernel=self.kernel,
                            response=function_to_execute(**context.function_kwargs),
                        )

                        output.append(response)
                        i += 1

                        if show_progress:
                            request.kernel.io.progress(length, i)

                        if isinstance(response, FailureResponse) and (
                            middleware.stop_on_failure
                            == MIDDLEWARE_OPTION_VALUE_ALLWAYS
                            or (
                                middleware.stop_on_failure
                                == MIDDLEWARE_OPTION_VALUE_OPTIONAL
                                and "stop_on_failure" in function_kwargs
                                and function_kwargs["stop_on_failure"]
                            )
                        ):
                            # "Stop" does not mean "fail", so we just stop the process.
                            return output

            # If only one response, return it directly instead of wrapping in MultipleResponse
            if len(output.responses) == 1:
                return output.responses[0]

            return output

        # Delegate context creation to resolver.
        context = request.resolver.build_execution_context(
            middleware=None,
            command_wrapper=self.command_wrapper,
            request=request,
            function_kwargs=function_kwargs,
        )

        # Use context.function if provided, otherwise use command's function
        function_to_execute = context.function or self.function

        return response_normalize(
            kernel=self.kernel, response=function_to_execute(**context.function_kwargs)
        )

    def _build_function_kwargs(self, request: CommandRequest) -> dict[str, Any]:
        from wexample_wex_core.exception.command_option_missing_exception import (
            CommandOptionMissingException,
        )

        # Allow middleware to add extra options.
        for middleware in self.command_wrapper.middlewares:
            middleware.append_options(
                request=request,
                command_wrapper=self.command_wrapper,
            )

        """Execute the command with the given request arguments."""
        # Parse and convert arguments to appropriate types
        parsed_args = self._parse_arguments(request.arguments)

        """Build the final kwargs dictionary for the function call."""
        function_kwargs = {}

        # Process all declared options
        for option in self.command_wrapper.options:
            value = None

            # If the option is in parsed args, use that value
            if option.name in parsed_args:
                value = parsed_args[option.name]
            # Otherwise, use the default value if available
            elif option.default is not None:
                value = option.default
            # If the option is required but not provided, raise an error
            elif option.required:
                raise CommandOptionMissingException(option_name=option.name)

            # Validate the value if validators are defined and value is not None
            if value is not None and option.validators:
                # For multiple values, validate each item individually
                values_to_validate = value if isinstance(value, list) else [value]

                for val in values_to_validate:
                    for validator in option.validators:
                        if not validator.validate(val):
                            from wexample_wex_core.exception.command_option_validation_exception import (
                                CommandOptionValidationException,
                            )

                            raise CommandOptionValidationException(
                                option_name=option.name,
                                value=val,
                                error_message=validator.get_error_message(val),
                            )

            # Normalize to list if always_list is True
            if value is not None and option.always_list and not isinstance(value, list):
                value = [value]

            # Assign the validated value
            if value is not None:
                option.value = function_kwargs[option.name] = value

        return function_kwargs

    async def _execute_passes_parallel(
        self, execution_contexts: list[ExecutionContext]
    ) -> list[Any]:
        """Execute multiple passes in parallel using asyncio.

        Args:
            execution_contexts: List of ExecutionPass objects to execute in parallel

        Returns:
            List of normalized responses from all executions
        """
        from concurrent.futures import ThreadPoolExecutor

        from wexample_app.helpers.response import response_normalize
        from wexample_app.response.abstract_response import AbstractResponse

        # Create a list to store all tasks
        tasks = []

        # Create an executor for running CPU-bound functions in a thread pool
        executor = ThreadPoolExecutor(max_workers=min(32, len(execution_contexts)))

        # Define a coroutine that executes a single pass
        async def execute_single_pass(
            execution_context: ExecutionContext,
        ) -> AbstractResponse:
            from wexample_prompt.output.prompt_buffer_output_handler import (
                PromptBufferOutputHandler,
            )

            output = PromptBufferOutputHandler()
            # Detach io manager to print log result at the end.
            execution_context._init_io_manager(output=output)

            # Use context.function if provided, otherwise use command's function
            function_to_execute = execution_context.function or self.function

            # Run the function in a thread pool to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                executor,
                lambda: function_to_execute(**execution_context.function_kwargs),
            )

            self.kernel.io.print_responses(output.buffer)

            # Normalize the response
            return response_normalize(kernel=self.kernel, response=result)

        # Create a task for each pass
        for execution_context in execution_contexts:
            task = asyncio.create_task(execute_single_pass(execution_context))
            tasks.append(task)

        # Wait for all tasks to complete
        responses = await asyncio.gather(*tasks)

        # Close the executor
        executor.shutdown(wait=False)

        return responses

    def _parse_arguments(self, arguments: list[str]) -> ParsedArgs:
        """Parse raw command line arguments into a dictionary of option name to value."""
        from wexample_app.helpers.argument import argument_parse_options

        return argument_parse_options(
            arguments=arguments,
            options=self.command_wrapper.options,
            allowed_option_names=self.command_wrapper.get_options_names(),
        )
