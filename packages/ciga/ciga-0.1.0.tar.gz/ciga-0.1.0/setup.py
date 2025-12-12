from setuptools import find_packages, setup
import os

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ciga',
    version='0.1.0',
    description='Character interaction temporal graph analysis',
    packages=find_packages(include=['ciga', 'ciga.*']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MediaCompLab/CIGA',
    author='Media Comprehension Lab',
    author_email='shu13@gsu.edu',
    # license='GPL-3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'igraph',
        'numpy',
        'tqdm',
        'matplotlib'
    ],
    extras_require={
        'all': ['anthropic', 'openai', 'pyvis>=0.3.0'],
        'dev': ['pytest>=7.0', 'twine>=4.0.2'],
        'visualization': ['pyvis>=0.3.0']
    },
    python_requires='>=3.6',
)
