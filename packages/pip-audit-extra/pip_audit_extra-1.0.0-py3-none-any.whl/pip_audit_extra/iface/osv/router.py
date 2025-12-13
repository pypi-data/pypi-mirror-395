from posixpath import join


class OSVRouter:
	def __init__(self, base_url: str = "https://api.osv.dev/v1/") -> None:
		self.base_url = base_url

	def vulnerability_detail(self, vuln_id: str) -> str:
		return join(self.base_url, "vulns", vuln_id)
