from typing import Final


PREFIX_HASH: Final[str] = "--hash"
PREFIX_COMMENT: Final[str] = "#"


def clean_requirements(requirements: str) -> str:
	"""
	Cleans project requirements.txt file content, removes hashes, comments and python versions.
	"""
	lines = requirements.split("\n")
	dependencies = []

	for line in lines:
		if line.lstrip().startswith((PREFIX_HASH, PREFIX_COMMENT)):
			continue

		line_parts = line.split(" ; ")
		dependencies.append(line_parts[0].strip().rstrip(" \\"))

	return "\n".join(dependencies)
