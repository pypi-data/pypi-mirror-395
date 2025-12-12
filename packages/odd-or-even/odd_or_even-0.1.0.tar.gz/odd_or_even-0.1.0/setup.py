# setup.py

from setuptools import setup, find_packages

setup(
    name='odd-or-even',  # The name of your package
    version='0.1.0',     # Version of your library
    description='A simple library to check if a number is odd or even.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ajay Antony Joseph',
    author_email='AJAYJOSEPH24@example.com',
    url='https://github.com/ajayjoseph13/odd-or-even',  # Replace with your GitHub repo URL
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
