from setuptools import setup, find_packages

setup(
    name='json-prettifier',
    version='0.1.0',
    description='A simple CLI tool to beautify and format JSON data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    url='https://github.com/yourusername/json-prettifier', # Replace with your repo URL
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',  # We need click for the CLI framework
    ],
    # Define the console scripts entry points
    entry_points={
        'console_scripts': [
            # jb = json_prettifier.cli:main
            'jb = json_prettifier.cli:main',
            # json-prettifier = json_prettifier.cli:main
            'json-prettifier = json_prettifier.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)