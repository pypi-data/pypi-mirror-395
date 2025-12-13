from typing import List


class DependencyVuln:
	__slots__ = "id", "aliases", "description", "fix_versions"

	id: str
	aliases: List[str]
	description: str
	fix_versions: List[str]

	def __init__(self, id: str, aliases: List[str], description: str, fix_versions: List[str]) -> None:
		self.id = id
		self.aliases = aliases
		self.description = description
		self.fix_versions = fix_versions

	@classmethod
	def from_dict(cls, d: dict) -> "DependencyVuln":
		return cls(
			id=d["id"],
			aliases=d["aliases"],
			description=d["description"],
			fix_versions=d["fix_versions"],
		)


class Dependency:
	__slots__ = "name", "version", "vulns"

	name: str
	version: str
	vulns: List[DependencyVuln]

	def __init__(self, name: str, version: str, vulns: List[DependencyVuln]) -> None:
		self.name = name
		self.version = version
		self.vulns = vulns

	@classmethod
	def from_dict(cls, d: dict) -> "Dependency":
		return cls(
			name=d["name"],
			version=d["version"],
			vulns=[DependencyVuln.from_dict(i) for i in d["vulns"]],
		)


class AuditReport:
	__slots__ = "dependencies"

	dependencies: List[Dependency]

	def __init__(self, dependencies: List[Dependency]) -> None:
		self.dependencies = dependencies

	@classmethod
	def from_dict(cls, d: dict) -> "AuditReport":
		dependencies = []

		for i in d.get("dependencies", []):
			if "skip_reason" in i:
				continue		# TODO: Collect skipped dependencies

			dependencies.append(Dependency.from_dict(i))

		return cls(dependencies=dependencies)
