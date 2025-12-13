from pip_audit_extra.generic.rich.time_elapsed_column import CustomTimeElapsedColumn

from typing import Optional, Type, Callable, Any
from contextlib import AbstractContextManager
from types import TracebackType

from rich.console import Console
from rich.text import Text
from rich.progress import Progress, TextColumn, BarColumn, TaskID
from rich.control import Control
from rich.segment import ControlType


class Printer(AbstractContextManager):
	"""
	A specialized class for rendering the audit process.
	"""
	def __init__(
		self,
		console: Console,
		*,
		print_table: Optional[Callable[[], Any]] = None,
		print_result: Optional[Callable[[], Any]] = None,
	) -> None:
		self.console = console
		self.progress = Progress(
			TextColumn("[progress.description]{task.description}"),
			BarColumn(),
			CustomTimeElapsedColumn(),
			transient=True,
		)
		self.task_id_main: Optional[TaskID] = None
		self.task_id_deps_collecting: Optional[TaskID] = None
		self.task_id_deps_checking: Optional[TaskID] = None
		self.task_id_vulns_inspecting: Optional[TaskID] = None

		self.print_table = print_table or self.noop
		self.print_result = print_result or self.noop

	def __enter__(self) -> "Printer":
		self.task_id_main = self.progress.add_task("Searching vulnerabilities...", total=None)
		self.progress.__enter__()
		return self

	def __exit__(
		self,
		exc_type: Optional[Type[BaseException]],
		exc_value: Optional[BaseException],
		traceback: Optional[TracebackType],
	) -> None:
		if self.task_id_main is not None and not any((exc_type, exc_value, traceback)):
			task_main = self.progress.tasks[self.task_id_main]
			self.progress.remove_task(self.task_id_main)
			column = CustomTimeElapsedColumn(style="white")
			# Rewriting the empty line that remains from the progress bar
			self.console.control(Control((ControlType.CURSOR_UP, 1)))
			self.print_table()
			self.print_result()
			self.console.print(Text("The audit was completed in"), column.render(task_main), style="white")

		return self.progress.__exit__(exc_type, exc_value, traceback)

	@staticmethod
	def noop(*args, **kwargs) -> None:
		pass

	def handle_collecting_start(self) -> None:
		self.task_id_deps_collecting = self.progress.add_task("Collecting dependencies...", total=None)

	def handle_collecting_end(self) -> None:
		if self.task_id_deps_collecting is not None:
			self.progress.remove_task(self.task_id_deps_collecting)

	def handle_checking_start(self, dependencies_count: int) -> None:
		self.task_id_deps_checking = self.progress.add_task("Checking dependencies...", total=dependencies_count)

	def handle_checking_step(self) -> None:
		if self.task_id_deps_checking is not None:
			self.progress.update(self.task_id_deps_checking, advance=1)

	def handle_checking_end(self) -> None:
		if self.task_id_deps_checking is not None:
			self.progress.remove_task(self.task_id_deps_checking)

	def handle_vulns_inspecting_start(self, vulnerabilities_count: int) -> None:
		self.task_id_vulns_inspecting = self.progress.add_task(
			"Inspecting vulnerabilities...",
			total=vulnerabilities_count,
		)

	def handle_vulns_inspecting_step(self) -> None:
		if self.task_id_vulns_inspecting is not None:
			self.progress.update(self.task_id_vulns_inspecting, advance=1)

	def handle_vulns_inspecting_end(self) -> None:
		if self.task_id_vulns_inspecting is not None:
			self.progress.remove_task(self.task_id_vulns_inspecting)
