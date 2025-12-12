from setuptools import setup, find_packages

setup(
    name='portableenv',
    version='2.0.3',
    author='AbdulRahim Khan',
    author_email='abdulrahimpds@gmail.com',
    description='A tool to create virtual environments using an embedded Python interpreter.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abdulrahimpds/portableenv',
    packages=find_packages(),
    install_requires=[
        'virtualenv',
        'click',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ],
    entry_points={
        'console_scripts': [
            'portableenv=portableenv.cli:main',
        ],
    },
    python_requires='>=3.7'
)