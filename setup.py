from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='rarce',
    version='1.0.0',
    author='Ata Hakcil',
    description='Exploit generator for CVE-2023-38831, WinRAR RCE.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rarce = rarce.cli:main'
        ]
    },
    install_requires=install_requires,
    keywords=['winrar', 'exploit', 'rce', 'cve-2023-38831']
)