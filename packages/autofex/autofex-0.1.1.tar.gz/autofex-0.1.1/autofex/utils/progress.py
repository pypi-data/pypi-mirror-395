"""
Progress Tracking and Real-Time Feedback

Provides progress tracking with real-time feedback for AutoFE-X operations.
"""

import time
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import sys


class ProgressTracker:
    """
    Progress tracker with real-time feedback for AutoFE-X operations.
    """

    def __init__(self, total_steps: int = 100, show_progress: bool = True):
        """
        Initialize progress tracker.

        Args:
            total_steps: Total number of steps
            show_progress: Whether to show progress bar
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.show_progress = show_progress
        self.start_time: Optional[float] = None
        self.step_times: List[float] = []
        self.step_names: List[str] = []
        self.messages: List[str] = []

    def start(self, message: str = "Starting..."):
        """
        Start progress tracking.

        Args:
            message: Initial message
        """
        self.start_time = time.time()  # type: ignore
        self.current_step = 0
        self.step_times = []
        self.step_names = []
        self.messages = []

        if self.show_progress:
            print(f"\n🚀 {message}")
            print("=" * 60)

    def update(
        self,
        step: int,
        message: str = "",
        step_name: Optional[str] = None,
        show_eta: bool = True,
    ):
        """
        Update progress.

        Args:
            step: Current step number
            message: Progress message
            step_name: Name of the step
            show_eta: Whether to show estimated time remaining
        """
        step_start = time.time()

        if step_name:
            self.step_names.append(step_name)

        if message:
            self.messages.append(message)

        self.current_step = step

        if self.show_progress:
            percentage = (step / self.total_steps) * 100 if self.total_steps > 0 else 0

            # Progress bar
            bar_length = 40
            filled = (
                int(bar_length * step / self.total_steps) if self.total_steps > 0 else 0
            )
            bar = "█" * filled + "░" * (bar_length - filled)

            # Time information
            elapsed = time.time() - self.start_time if self.start_time else 0

            if show_eta and step > 0 and self.total_steps > 0:
                avg_time_per_step = elapsed / step
                remaining_steps = self.total_steps - step
                eta = avg_time_per_step * remaining_steps
                eta_str = f" | ETA: {self._format_time(eta)}"
            else:
                eta_str = ""

            # Print progress
            progress_line = f"\r[{bar}] {percentage:5.1f}% | Step {step}/{self.total_steps} | Elapsed: {self._format_time(elapsed)}{eta_str}"

            if message:
                progress_line += f" | {message}"

            sys.stdout.write(progress_line)
            sys.stdout.flush()

        step_time = time.time() - step_start
        self.step_times.append(step_time)

    def finish(self, message: str = "Complete!"):
        """
        Finish progress tracking.

        Args:
            message: Completion message
        """
        total_time = time.time() - self.start_time if self.start_time else 0

        if self.show_progress:
            print()  # New line after progress bar
            print("=" * 60)
            print(f"✅ {message}")
            print(f"⏱️  Total time: {self._format_time(total_time)}")

            if self.step_times:
                avg_step_time = sum(self.step_times) / len(self.step_times)
                print(f"📊 Average step time: {self._format_time(avg_step_time)}")
                print(f"📈 Total steps: {len(self.step_times)}")

        return {
            "total_time": total_time,
            "step_times": self.step_times,
            "step_names": self.step_names,
            "messages": self.messages,
        }

    def _format_time(self, seconds: float) -> str:
        """Format time in human-readable format."""
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.1f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours}h {minutes}m {secs:.1f}s"

    def log(self, message: str, level: str = "INFO"):
        """
        Log a message.

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        self.messages.append(log_message)

        if self.show_progress:
            print(f"\n{log_message}")


class RealTimeFeedback:
    """
    Real-time feedback system for long-running operations.
    """

    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize real-time feedback.

        Args:
            callback: Optional callback function for custom feedback handling
        """
        self.callback = callback
        self.metrics: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []

    def update_metric(self, name: str, value: Any, timestamp: Optional[float] = None):
        """
        Update a metric.

        Args:
            name: Metric name
            value: Metric value
            timestamp: Optional timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()

        self.metrics[name] = {
            "value": value,
            "timestamp": timestamp,
        }

        self.history.append(
            {
                "name": name,
                "value": value,
                "timestamp": timestamp,
            }
        )

        if self.callback:
            self.callback(name, value, timestamp)

    def get_metric(self, name: str) -> Optional[Any]:
        """
        Get current value of a metric.

        Args:
            name: Metric name

        Returns:
            Current metric value or None
        """
        if name in self.metrics:
            return self.metrics[name]["value"]
        return None

    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all current metrics.

        Returns:
            Dictionary of all metrics
        """
        return {name: data["value"] for name, data in self.metrics.items()}

    def get_history(self, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get metric history.

        Args:
            name: Optional metric name to filter by

        Returns:
            List of metric updates
        """
        if name:
            return [h for h in self.history if h["name"] == name]
        return self.history

    def print_summary(self):
        """Print summary of all metrics."""
        print("\n📊 Real-Time Metrics Summary:")
        print("-" * 60)
        for name, data in self.metrics.items():
            print(f"  • {name}: {data['value']}")
        print("-" * 60)
