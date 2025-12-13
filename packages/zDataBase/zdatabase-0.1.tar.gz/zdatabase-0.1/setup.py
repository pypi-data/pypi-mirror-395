from setuptools import setup, find_packages

setup(
    name="zDataBase",
    version="0.1",
    author="seyyed mohamad hosein moosavi raja(01)",
    author_email="mohamadhosein159159@gmail.com",
    description="This project is designed to simplify working with the sqlite3 database, offers extensive features, and supports all types in Python.",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OandONE/zdb",
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        "aiosqlite" # sqlite3 asynco
    ],
    license="MIT"
)