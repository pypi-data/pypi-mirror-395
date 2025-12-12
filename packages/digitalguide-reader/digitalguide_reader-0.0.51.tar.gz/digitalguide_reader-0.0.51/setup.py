from setuptools import find_packages, setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='digitalguide_reader',
    packages=find_packages(),
    version='0.0.51',
    description='A Python Library to read in a google sheet and turn it into states and actions',
    author='Soeren Etler',
    license='MIT',
    install_requires=["openpyxl",
                      "PyYAML",
                      "requests",
                      "google-api-python-client",
                      "google-auth-httplib2",
                      "google-auth-oauthlib"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'gsheet2route = digitalguide_reader.gsheet2actions:gsheet2actions',
            'route2mongodb = digitalguide_reader.upload_route:upload_route'
        ]
    }
)
