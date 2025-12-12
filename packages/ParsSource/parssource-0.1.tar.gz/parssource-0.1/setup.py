from setuptools import setup, find_packages

setup(
    name="ParsSource",
    version="0.1",
    author="seyyed mohamad hosein moosavi raja(01)",
    author_email="mohamadhosein159159@gmail.com",
    description="the library SPlus platform for bots.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OandONE/SPlus",
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=["httpx"],
    license="MIT"
)