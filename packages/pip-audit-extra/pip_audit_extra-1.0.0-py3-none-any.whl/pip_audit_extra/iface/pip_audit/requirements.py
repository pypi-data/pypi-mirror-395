from pip_audit_extra.iface.pip_audit.base import PIPAudit, AuditPreferences

from subprocess import run, CompletedProcess
from tempfile import NamedTemporaryFile
from os import remove


class AuditPreferencesRequirements(AuditPreferences):
	"""
	Audit preferences dataclass.

	Attrs:
		requirements: Project dependencies in the `requirements.txt` format.
		timeout: (in seconds) Max audit execution time.
		disable_pip: allows to skip dependency resolution stage with using requirements hashes.
	"""
	__slots__ = "timeout", "requirements", "disable_pip"

	requirements: str
	disable_pip: bool

	def __init__(self, requirements: str, *, disable_pip: bool = False, timeout: float = 600):
		super().__init__(timeout=timeout)
		self.requirements = requirements
		self.disable_pip = disable_pip


class PIPAuditRequirements(PIPAudit):
	def audit(self, preferences: AuditPreferencesRequirements) -> CompletedProcess:
		tmpfile = NamedTemporaryFile("w", delete=False)
		command = ["pip-audit", "-f", "json", "--progress-spinner", "off", "-r", tmpfile.name]

		if preferences.disable_pip:
			command.append("--disable-pip")

		try:
			tmpfile.write(preferences.requirements)
			tmpfile.close()
			completed_process = run(command, capture_output=True, encoding="utf-8", timeout=preferences.timeout)
		finally:
			remove(tmpfile.name)

		return completed_process
