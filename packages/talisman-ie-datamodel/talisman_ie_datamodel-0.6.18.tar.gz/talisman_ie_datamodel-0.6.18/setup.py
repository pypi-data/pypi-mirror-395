from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-ie-datamodel',
    version=version,
    description='Talisman-IE Document Model',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['tie_datamodel', 'tie_datamodel.*']),
    install_requires=[
        'talisman-interfaces>=0.11.9,<0.12', 'talisman-dm>=1.3.4,<2',
        'immutabledict>=2.2.4,<3', 'intervaltree~=3.1',
        'pydantic~=2.5', 'typing_extensions>=4.0.0',
        'aiofiles>=24.1.0'
    ],
    entry_points={
        'talisman.plugins': ['tie = tie_datamodel']
    },
    extras_require={
        'tests': {'talisman-tools'}
    },
    data_files=[('', ['VERSION'])],
    python_requires='>=3.10',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
