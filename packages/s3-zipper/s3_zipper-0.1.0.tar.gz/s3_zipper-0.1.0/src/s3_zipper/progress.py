import time
from .logger import logger

class ProgressTracker:
    """
    Lightweight progress printer for streaming operations.

    Prints progress every `chunk_step_bytes` to avoid log spam.
    """

    def __init__(self, total_bytes: int, label: str, chunk_step_mb: int = 10):
        self.total_bytes = total_bytes
        self.label = label

        # Print step in bytes (default: 10 MB)
        self.chunk_step = chunk_step_mb * 1024 * 1024

        self.bytes_processed = 0
        self.next_mark = self.chunk_step

        self.start_time = time.time()

        logger.info(f"[{self.label}] Starting… Total size: {self._fmt(total_bytes)}")

    def update(self, n: int):
        """Add n bytes to progress."""
        self.bytes_processed += n

        if self.bytes_processed >= self.next_mark:
            pct = (self.bytes_processed / self.total_bytes) * 100 if self.total_bytes > 0 else 0
            logger.info(
                f"[{self.label}] {self._fmt(self.bytes_processed)} / "
                f"{self._fmt(self.total_bytes)}  ({pct:5.1f}%)"
            )
            self.next_mark += self.chunk_step

    def finish(self):
        elapsed = time.time() - self.start_time
        logger.info(
            f"[{self.label}] Completed: {self._fmt(self.bytes_processed)} "
            f"in {elapsed:.2f}s"
        )

    def _fmt(self, num_bytes: int) -> str:
        """Format bytes into KB/MB/GB with units."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if num_bytes < 1024:
                return f"{num_bytes:.1f}{unit}"
            num_bytes /= 1024
        return f"{num_bytes:.1f}PB"
