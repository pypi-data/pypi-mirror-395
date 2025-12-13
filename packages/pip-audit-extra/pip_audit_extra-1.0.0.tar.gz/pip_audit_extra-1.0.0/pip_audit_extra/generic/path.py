from platform import system
from os import getenv
from os.path import expanduser, join


def get_cache_path() -> str:
	"""
	Returns path to user cache folder.

	Warnings:
		* Not tested on Darwin.
	"""
	if system() == "Windows":
		if path := getenv("LOCALAPPDATA"):
			return path
		else:
			home_path = expanduser("~")
			return join(home_path, "AppData", "Local")

	else:
		return join(expanduser("~"), ".cache")
