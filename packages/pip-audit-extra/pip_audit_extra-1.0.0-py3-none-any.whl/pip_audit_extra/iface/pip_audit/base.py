from pip_audit_extra.iface.pip_audit.dataclass import AuditReport

from abc import ABC, abstractmethod
from subprocess import CompletedProcess
from json import loads


class AuditPreferences:
	"""
	Audit preferences dataclass.

	Attrs:
		timeout: (in seconds) Max audit execution time.
	"""
	__slots__ = "timeout"

	timeout: float

	def __init__(self, *, timeout: float = 600):
		self.timeout = timeout


class PIPAudit(ABC):
	def run(self, preferences: AuditPreferences) -> AuditReport:
		completed_process = self.audit(preferences)
		return self.audit_postprocess(completed_process)

	@abstractmethod
	def audit(self, preferences: AuditPreferences) -> CompletedProcess: ...

	def audit_postprocess(self, completed_process: CompletedProcess) -> AuditReport:
		if completed_process.returncode not in {0, 1}:
			raise RuntimeError(f"pip-audit returned an unexpected code: {completed_process.returncode}")

		report = loads(completed_process.stdout)

		if not isinstance(report, dict):
			raise ValueError("Deserialized report must be of dict type")

		return AuditReport.from_dict(report)
