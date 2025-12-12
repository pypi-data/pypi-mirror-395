"""Models to support telemetry data."""

from pydantic import BaseModel


class ObservableProgress(BaseModel, validate_assignment=True):
    """Container for tracking progress for a metering instrument e.g. task progress."""

    current: int = 0
    total: int = 0

    def increment(self, step: int = 1) -> None:
        """Increment the current progress by the given step."""
        self.current += step

    @property
    def percent_complete(self) -> float:
        """Return the percent complete as a float between 0 and 100."""
        if self.total > 0:
            return (self.current / self.total) * 100
        return 0.0

    def set_complete(self):
        """Set the current progress to the total."""
        if self.total == 0:
            self.total = self.current = 1
        else:
            self.current = self.total
