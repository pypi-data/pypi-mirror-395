from pip_audit_extra.severity import Severity
from pip_audit_extra.iface.pip_audit import (
	AuditPreferences, PIPAuditRequirements, AuditPreferencesRequirements, PIPAuditLocal, DependencyVuln,
)
from pip_audit_extra.iface.osv import OSVService
from pip_audit_extra.vulnerability.dataclass import Vulnerability
from pip_audit_extra.vulnerability.cache import Cache, VulnerabilityData
from pip_audit_extra.requirement import clean_requirements

from typing import Generator, Final, Optional, Callable, Any
from warnings import warn
from datetime import timedelta


VULN_ID_PREFIX_PYSEC: Final[str] = "PYSEC"
VULN_ID_PREFIX_GHSA: Final[str] = "GHSA"


class Auditor:
	def __init__(
		self,
		cache_lifetime: Optional[timedelta],
		local: bool = False,
		disable_pip: bool = False,
		*,
		on_collecting_start: Optional[Callable[[], Any]] = None,
		on_collecting_end: Optional[Callable[[], Any]] = None,
		on_checking_start: Optional[Callable[[int], Any]] = None,
		on_checking_step: Optional[Callable[[], Any]] = None,
		on_checking_end: Optional[Callable[[], Any]] = None,
		on_inspecting_start: Optional[Callable[[int], Any]] = None,
		on_inspecting_step: Optional[Callable[[], Any]] = None,
		on_inspecting_end: Optional[Callable[[], Any]] = None,
	) -> None:
		self.osv_service = OSVService()
		self.cache = Cache(lifetime=cache_lifetime)
		self.local = local
		self.disable_pip = disable_pip

		self.on_collecting_start = on_collecting_start or self.noop
		self.on_collecting_end = on_collecting_end or self.noop
		self.on_checking_start = on_checking_start or self.noop
		self.on_checking_step = on_checking_step or self.noop
		self.on_checking_end = on_checking_end or self.noop
		self.on_inspecting_start = on_inspecting_start or self.noop
		self.on_inspecting_step = on_inspecting_step or self.noop
		self.on_inspecting_end = on_inspecting_end or self.noop

	@staticmethod
	def noop(*args, **kwargs) -> None:
		return None

	def audit(self, requirements: str) -> Generator[Vulnerability, None, None]:
		"""
		Performs project dependencies audit.

		Args:
			requirements: Project dependencies in the `requirements.txt` format.

		Yields:
			Vulnerability objects.
		"""
		if self.local:
			preferences = AuditPreferences()
			audit_strategy_cls = PIPAuditLocal
		else:
			if not self.disable_pip:
				requirements = clean_requirements(requirements)

			preferences = AuditPreferencesRequirements(requirements, disable_pip=self.disable_pip)
			audit_strategy_cls = PIPAuditRequirements

		self.on_collecting_start()

		pip_audit = audit_strategy_cls()
		audit_report = pip_audit.run(preferences)

		self.on_collecting_end()
		self.on_checking_start(len(audit_report.dependencies))

		for dependency in audit_report.dependencies:
			self.on_inspecting_start(len(dependency.vulns))

			for vuln in dependency.vulns:
				try:
					severity = self.get_severity(vuln)
				except Exception as err:
					warn(f"Could not get information about {vuln.id} vulnerability. Error: {err}")
					continue
				finally:
					self.on_inspecting_step()

				yield Vulnerability(
					id=vuln.id,
					package_name=dependency.name,
					package_version=dependency.version,
					fix_versions=vuln.fix_versions,
					severity=severity,
				)

			self.on_inspecting_end()
			self.on_checking_step()

		self.on_checking_end()
		self.cache.save()

	def get_severity(self, vuln: DependencyVuln) -> Optional[Severity]:
		if vuln_data := self.cache.get(vuln.id):
			raw_severity = vuln_data.severity
		else:
			vuln_details = self.osv_service.get_vulnerability(vuln.id)

			if vuln.id.startswith(VULN_ID_PREFIX_PYSEC):
				for alias in vuln_details.get("aliases", []):
					if alias.startswith(VULN_ID_PREFIX_GHSA):
						vuln_details = self.osv_service.get_vulnerability(alias)		# GHSAs have severity
						break

			raw_severity = vuln_details.get("database_specific", {}).get("severity")
			self.cache.add(VulnerabilityData(vuln.id, vuln.fix_versions, raw_severity))

		if raw_severity:
			return Severity(raw_severity)

		return None
