from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-ie-rubricator',
    version=version,
    description='Talisman-IE toolkit for automatic rubrication',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['tie_rubricator', 'tie_rubricator.*']),
    install_requires=[
        'talisman-interfaces>=0.11.8,<0.12',
        'talisman-api~=1.4',
        'talisman-domain~=0.4.8',
        'talisman-dm>=1.3.8,<2'
    ],
    extras_require={},
    data_files=[('', ['VERSION'])],
    package_data={
        'tie_rubricator.provider.api._impl': ['graphql/**/*']
    },
    python_requires='>=3.10',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
