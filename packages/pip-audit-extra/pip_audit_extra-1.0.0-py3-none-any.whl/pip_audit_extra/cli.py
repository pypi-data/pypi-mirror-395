from pip_audit_extra.vulnerability.filter.severity import SeverityFilterOption
from pip_audit_extra.severity import Severity

from argparse import ArgumentParser, ArgumentTypeError
from typing import Optional, Any, Final
from datetime import timedelta
from re import compile, Pattern, IGNORECASE


FILTER_PREFIX_EXAC: Final[str] = "~"
LIFETIME_RE: Final[Pattern] = compile(r"^\d+[dhms]$", IGNORECASE)


class SeverityFilterHandler:
	"""
	Converts value to optional SeverityFilterOption object.
	"""
	def __init__(self) -> None:
		self.severity_names = set(Severity.get_names())

	def __call__(self, value: Any) -> Optional[SeverityFilterOption]:
		if value is None:
			return value

		if not isinstance(value, str):
			raise ArgumentTypeError("Value must be str or None")

		if value.startswith(FILTER_PREFIX_EXAC):
			return SeverityFilterOption(True, self.get_severity(value.lstrip(FILTER_PREFIX_EXAC)))

		return SeverityFilterOption(False, self.get_severity(value))

	def get_severity(self, severity_name: str) -> Severity:
		severity_name = severity_name.upper()

		if severity_name not in self.severity_names:
			raise ArgumentTypeError("Unknown severity was met")

		return Severity[severity_name]


class FailLevelHandler:
	def __call__(self, value: Any) -> Optional[Severity]:
		if value is None:
			return value

		if not isinstance(value, str):
			raise ArgumentTypeError("Value must be str or None")

		try:
			return Severity[value.upper()]
		except Exception as err:
			raise ArgumentTypeError("Unknown severity was met") from err


class CacheLifetimeHandler:
	def __call__(self, value: Any) -> Optional[timedelta]:
		if value is None:
			return value

		if not isinstance(value, str):
			raise ArgumentTypeError("Value must be str or None")

		if value.isdigit():
			return timedelta(seconds=int(value))

		elif LIFETIME_RE.match(value):
			count, unit = int(value[:-1]), value[-1].lower()

			if unit == "d":
				return timedelta(days=count)
			elif unit == "h":
				return timedelta(hours=count)
			elif unit == "m":
				return timedelta(minutes=count)
			elif unit == "s":
				return timedelta(seconds=count)

		raise ArgumentTypeError("Value must be string in format: '<int>[d,h,m,s]'")


def get_parser() -> ArgumentParser:
	parser = ArgumentParser(
		"pip-audit-extra",
		description="An add-on to the pip-audit utility, which allows to work with vulnerabilities of a certain severity",
	)
	parser.add_argument(
		"--severity",
		type=SeverityFilterHandler(),
		default=None,
		help=f"""\
vulnerability filter by severity.
Possible values: {', '.join(Severity.get_names())}.
By default, the filter selects vulnerabilities with the specified severity AND SEVERITIES WITH A HIGHER PRIORITY.
To select only the specified level, add the prefix `~`, for example `--severity ~HIGH`.
It only affects the vulnerability table.\
""",
	)
	parser.add_argument(
		"--fail-level",
		type=FailLevelHandler(),
		default=None,
		help=f"""\
severity of vulnerability from which the audit will be considered to have failed.
Possible values: {', '.join(Severity.get_names())}.
Affects the audit result.\
""",
	)
	parser.add_argument(
		"--cache-lifetime",
		type=CacheLifetimeHandler(),
		default="1d",
		help="""\
lifetime of each record in cache.
Supported formats:
* <int> - seconds;
* <int>d - days;
* <int>h - hours;
* <int>m - minutes;
* <int>s - seconds.

Example 1: 12h
Example 2: 43200\
""",
	)
	parser.add_argument(
		"--local",
		default=False,
		action="store_true",
		help="""
analyze packages installed in the current local environment.
"""
	)
	parser.add_argument(
		"--disable-pip",
		default=False,
		action="store_true",
		help="""
don't use `pip` for dependency resolution; this can only be used with hashed requirements files.
"""
	)

	return parser
