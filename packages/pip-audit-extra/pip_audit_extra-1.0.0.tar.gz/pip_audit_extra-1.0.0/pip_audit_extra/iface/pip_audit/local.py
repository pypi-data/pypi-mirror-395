from pip_audit_extra.iface.pip_audit.base import AuditPreferences, PIPAudit

from subprocess import run, CompletedProcess


class PIPAuditLocal(PIPAudit):
	def audit(self, preferences: AuditPreferences) -> CompletedProcess:
		return run(
			["pip-audit", "-f", "json", "--progress-spinner", "off", "-l"],
			capture_output=True,
			encoding="utf-8",
			timeout=preferences.timeout,
		)
