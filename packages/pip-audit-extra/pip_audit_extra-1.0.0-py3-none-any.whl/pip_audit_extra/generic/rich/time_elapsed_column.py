from typing import Optional
from datetime import timedelta

from rich.text import Text
from rich.table import Column
from rich.progress import TimeElapsedColumn, Task



class CustomTimeElapsedColumn(TimeElapsedColumn):
	def __init__(self, table_column: Optional[Column] = None, style: str = "progress.elapsed") -> None:
		super().__init__(table_column)
		self.style = style

	def render(self, task: Task):
		elapsed = task.finished_time if task.finished else task.elapsed

		if elapsed is None:
			return Text("--", style=self.style)

		delta = timedelta(milliseconds=max(0, int(elapsed * 1000)))

		return Text(self.render_delta(delta), style=self.style)

	def render_delta(self, delta: timedelta) -> str:
		return f"{delta.total_seconds():0.1f}s"
