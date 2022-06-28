from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in practice_manager/__init__.py
from practice_manager import __version__ as version

setup(
	name="practice_manager",
	version=version,
	description="This app will be used by different service providers to record their services offered to various customers, record billed amounts and track invoice\'s payment status. The system will also auto email statements to the various customers and the service provider is able to track their ledgers. Initially to be used in healthcare settings but can work in other sectors as well.",
	author="Lonius Limited",
	author_email="info@lonius.co.ke",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
