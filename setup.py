from setuptools import setup, find_packages

setup(
    name='NetMermaid',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'networkx',
        'plotly',
        'pycountry',
        'emoji',
    ],
    author='Your Name',
    author_email='your_email@example.com',
    description='A package to visualize IP communications over time using Mermaid or NetworkX.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NetMermaid',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
