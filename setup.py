import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storageapi",
    version="0.0.1",
    author="Tobias Schoch",
    author_email="reza@cpol.co",
    packages=setuptools.find_packages('api', include=('models', 'client')),
    description="Python client for the storageapi",
    long_description=long_description,
    long_description_content_type="text/x-restructured",
    url="https://github.com/toschoch/python-storageapi",
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
         "requests",
    ]
)
