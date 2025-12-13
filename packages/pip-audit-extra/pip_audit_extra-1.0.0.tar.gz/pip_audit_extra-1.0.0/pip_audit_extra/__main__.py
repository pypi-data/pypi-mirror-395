from pip_audit_extra.cli import get_parser
from pip_audit_extra.auditor import Auditor
from pip_audit_extra.vulnerability.print import print_vulnerabilities
from pip_audit_extra.vulnerability.filter.filter import VulnerabilityFilter
from pip_audit_extra.vulnerability.filter.severity import SeverityChecker
from pip_audit_extra.printer import Printer

from sys import exit, argv, stdin
from functools import partial

from rich.console import Console


def main() -> int:
	parser = get_parser()
	namespace = parser.parse_args(argv[1:])
	vulnerability_filter = VulnerabilityFilter(severity=namespace.severity)

	if namespace.local:
		requirements = ""
	else:
		requirements = stdin.read()

	auditor = Auditor(cache_lifetime=namespace.cache_lifetime, local=namespace.local, disable_pip=namespace.disable_pip)

	with Console() as console:
		with Printer(console) as printer:
			auditor.on_collecting_start = printer.handle_collecting_start
			auditor.on_collecting_end = printer.handle_collecting_end
			auditor.on_checking_start = printer.handle_checking_start
			auditor.on_checking_step = printer.handle_checking_step
			auditor.on_checking_end = printer.handle_checking_end
			auditor.on_inspecting_start = printer.handle_vulns_inspecting_start
			auditor.on_inspecting_step = printer.handle_vulns_inspecting_step
			auditor.on_inspecting_end = printer.handle_vulns_inspecting_end
			vulns = [*auditor.audit(requirements)]

			if filtered_vulns := [*vulnerability_filter.filter(vulns)]:
				printer.print_table = partial(print_vulnerabilities, console, filtered_vulns)

			if vulns and namespace.fail_level is None:
				return 1

			severity_checker = SeverityChecker(namespace.fail_level)

			if any(map(severity_checker.check, vulns)):
				return 1

			if vulns:
				printer.print_result = partial(
					console.print,
					"[green]✨ No vulnerabilities leading to failure found ✨[/green]",
				)
			else:
				printer.print_result = partial(
					console.print,
					"[green]✨ No vulnerabilities found ✨[/green]",
				)

	return 0


if __name__ == "__main__":
	exit(main())
