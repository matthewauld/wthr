import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wthr", # Replace with your own username
    version="0.0.1",
    author="Matthew Auld",
    author_email="matthew@matthewauld.ca",
    description="displays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewauld/wthr",
    packages=['wthr'],
    scripts=['bin/wthr'],
    license="LICENSE.txt",
    install_requires =["atoma>=0.0.17","requests>=2.23.0"],
    python_requires='>=3.6',
    )
