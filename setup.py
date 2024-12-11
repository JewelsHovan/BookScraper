from setuptools import setup, find_namespace_packages

setup(
    name='bookscraper',
    version='0.1.0',
    packages=find_namespace_packages(include=['src*']),
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=[
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'lxml>=4.9.3',
        'urllib3>=2.0.7',
        'tqdm>=4.66.1',
        'aiohttp>=3.8.5',
        'tenacity>=8.2.3',
        'click>=8.1.7',
        'PyYAML>=6.0.1',
        'rich>=13.5.2',
        "fickling>=0.1.3,~=0.1.0",
    ],
    entry_points={
        'console_scripts': [
            'bookscraper=src.cli.main:cli',
        ],
    },
)
