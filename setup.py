from setuptools import find_packages, setup


setup(
      name="pytoolbase",
      version="0.4",
      description="Python Utilities",
      author="Simone Mozzaia",
      author_email='info@simonemozzaia.it"',
      platforms=["win32"],  # or more specific, e.g. "win32", "cygwin", "osx"
      license="GPLv3",
      url="https://github.com/SimoneMozzaia/pythoolbase",
      packages=find_packages(),
      include_package_data=True
)
