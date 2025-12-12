from __future__ import annotations


class HasLogHandler:
    def _handle_logs(self, logger_name, callback):
        """
        Capture logs from a specific logger and process them with a callback.

        Args:
            logger_name: Name of the logger to capture
            callback: Function to call with each log line
        """
        import io
        import logging
        from contextlib import contextmanager

        @contextmanager
        def log_handler() -> None:
            # Create a custom handler to capture log messages
            log_capture = io.StringIO()

            # Get the logger and configure it
            logger = logging.getLogger(logger_name)
            original_level = logger.level
            logger.setLevel(logging.WARNING)

            # Add a handler that writes to our StringIO
            handler = logging.StreamHandler(log_capture)
            logger.addHandler(handler)

            try:
                # Return the configured objects for use in a with statement
                yield log_capture
            finally:
                # Process captured logs
                log_output = log_capture.getvalue()
                if log_output:
                    for line in log_output.strip().split("\n"):
                        if line:
                            callback(line)

                # Clean up: remove the handler and restore the original log level
                logger.removeHandler(handler)
                logger.setLevel(original_level)

        return log_handler()
