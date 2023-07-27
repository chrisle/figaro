from setuptools import find_packages, setup

setup(
    name='figaro',
    version='0.0.1',
    url='https://somethinghere.com',
    author='Chris Le',
    author_email='christopher.le@accenture.com',
    description='Prompting engine for large language models',
    long_description='Prompting engine for large language models',
    packages=find_packages(include=['figaro']),
    install_requires=[
        'google-cloud-aiplatform',
        'jinja2',
        'pydantic',
        'requests',
        'pytz',
    ]
)