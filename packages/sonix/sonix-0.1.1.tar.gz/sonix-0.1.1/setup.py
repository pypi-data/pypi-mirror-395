from pathlib import Path
from setuptools import setup
from sonix import __version__
from pkg_resources import parse_requirements


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sonix',
    version=__version__,
    url='https://github.com/dimastatz/sonix',
    author='Dima Statz',
    author_email='dima.statz@gmail.com',
    packages=['sonix'],
    python_requires=">=3.8",
    install_requires=[
        str(r)
        for r in parse_requirements(
            Path(__file__).with_name("requirements.txt").open()
        )
    ],
    description="Sonix: extract rich analytical signals directly from audio files",
    long_description = long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'': ['static/*']},
)