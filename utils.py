from datetime import datetime


class Logger:
    # Log levels
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    # Source identifiers
    PLAYER = "PLAYER"
    GAME = "GAME"
    SERVER = "SERVER"
    SYSTEM = "SYSTEM"

    def __init__(
        self, log_to_console=True, log_to_file=False, log_file="grindstone.log"
    ):
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_file = log_file
        self.logs = []

    def log(self, source, level, message, data=None):
        """Create a formatted log entry

        Args:
            source: Who triggered the action (PLAYER, GAME, SERVER, SYSTEM)
            level: Status level (INFO, SUCCESS, WARNING, ERROR, CRITICAL)
            message: Main log message
            data: Optional dictionary of additional relevant data
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format: [TIMESTAMP] [SOURCE] [LEVEL] Message {Data if present}
        log_entry = f"[{timestamp}] [{source}] [{level}] {message}"

        # Add data if provided
        if data:
            data_str = " ".join([f"{k}={v}" for k, v in data.items()])
            log_entry += f" {{{data_str}}}"

        # Store log
        self.logs.append(log_entry)

        # Output to console if enabled
        if self.log_to_console:
            print(log_entry)

        # Write to file if enabled
        if self.log_to_file:
            with open(self.log_file, "a") as f:
                f.write(log_entry + "\n")

        return log_entry

    # Convenience methods for different log types
    def info(self, source, message, data=None):
        return self.log(source, self.INFO, message, data)

    def player_action(self, action, message, data=None):
        return self.log(self.PLAYER, self.INFO, f"{action}: {message}", data)

    def game_event(self, event, message, data=None):
        return self.log(self.GAME, self.INFO, f"{event}: {message}", data)

    def server_event(self, event, message, data=None):
        return self.log(self.SERVER, self.INFO, f"{event}: {message}", data)

    def system_event(self, event, message, data=None):
        return self.log(self.SYSTEM, self.INFO, f"{event}: {message}", data)

    def success(self, source, message, data=None):
        return self.log(source, self.SUCCESS, message, data)

    def warning(self, source, message, data=None):
        return self.log(source, self.WARNING, message, data)

    def error(self, source, message, data=None):
        return self.log(source, self.ERROR, message, data)

    def critical(self, source, message, data=None):
        return self.log(source, self.CRITICAL, message, data)

    def get_logs(self):
        """Return all stored logs"""
        return self.logs.copy()

    def clear_logs(self):
        """Clear stored logs"""
        self.logs = []


# Utility functions can be added here as needed
