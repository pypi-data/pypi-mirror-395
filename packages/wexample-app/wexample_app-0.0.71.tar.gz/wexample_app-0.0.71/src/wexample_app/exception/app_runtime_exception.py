from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_app.common.abstract_kernel import AbstractKernel


class AppRuntimeException(UndefinedException):
    """Base exception for expected runtime errors in the application.

    This exception class is used for errors that are part of normal application
    flow and should not display a full traceback. These are business logic errors
    that should be handled gracefully and displayed to the user in a friendly way.

    Examples include:
    - Command not found
    - Invalid configuration
    - Missing required resources

    Subclasses of this exception can be caught specifically to provide
    custom error handling without showing technical stack traces.
    """

    error_code: str = "APP_RUNTIME_ERROR"

    def format_error_with_kernel(self, kernel: AbstractKernel) -> None:
        """Format and display the exception using the kernel's error system.

        This method handles the presentation of runtime errors in a user-friendly way,
        displaying the main error message and logging additional context data.

        Args:
            kernel: The kernel instance to use for error display and logging
        """
        # Display the main error message
        kernel.error(message=f"Runtime error: {self.message}")

        # Log additional context data if available
        if self.data:
            kernel.log(f"Error details: {self.error_code}", indentation=1)
            for key, value in self.data.items():
                kernel.log(message=f"  {key}: {value}", indentation=1)
