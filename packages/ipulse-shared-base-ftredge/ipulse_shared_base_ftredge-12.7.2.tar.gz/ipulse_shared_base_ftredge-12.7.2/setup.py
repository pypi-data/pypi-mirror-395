# pylint: disable=import-error
from setuptools import setup, find_packages

setup(
    name='ipulse_shared_base_ftredge',
    version='12.7.2',
    package_dir={'': 'src'},  # Specify the source directory
    packages=find_packages(where='src'),  # Look for packages in 'src'
    include_package_data=True,
    install_requires=[
        # List your dependencies here
        'google-cloud-logging~=3.12.1',
        'google-cloud-error-reporting~=1.12.0',
        'Cerberus~=1.3.7',
    ],
    author='Russlan Ramdowar',
    description='Shared Enums, Logger and other Base Utils for  Pulse Platform . Using AI for Asset Management and Financial Advisory.',
    url='https://github.com/TheFutureEdge/ipulse_shared_base',
)