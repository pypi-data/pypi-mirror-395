# pylint: disable=import-error
from setuptools import setup, find_packages

setup(
    name='ipulse-shared-data-eng-ftredge',
    version="12.8.6",
    package_dir={'': 'src'},  # Specify the source directory
    packages=find_packages(where='src'),  # Look for packages in 'src'
    install_requires=[
        # List your dependencies here
        'ipulse_shared_base_ftredge~=12.7.2', ##contains google cloud logging and error reporting
        'python-dateutil~=2.9.0',
        'pydantic~=2.11.7',  # Required for BaseModel support in Firestore operations
        # 'pytest~=7.1', # only used for testing , for which data_eng env is used anyway
        # 'Cerberus~=1.3.5', #already in ipulse_shared_base_ftredge
        # 'google-crc32c==1.6.0'
        'google-cloud-bigquery~=3.34.0',
        'google-cloud-storage>=2.18.0',
        'google-cloud-pubsub~=2.30.0',
        'google-cloud-secret-manager~=2.24.0',
        'google-cloud-firestore~=2.21.0',
        
    ],
    author='Russlan Ramdowar',
    description='Shared Data Engineering functions for the Pulse platform project. Using AI for financial advisory and investment management.',
    url='https://github.com/TheFutureEdge/ipulse_shared_data_eng'
)
