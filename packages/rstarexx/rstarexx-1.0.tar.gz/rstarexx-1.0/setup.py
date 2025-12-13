from setuptools import setup, find_packages

setup(
    name="rstarexx",
    version="1.0",
    author="Starexx",
    author_email="starexx.m@gmail.com",
    description="Termux command execution server",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["Flask>=2.0.0"],
    entry_points={
        "console_scripts": ["starexx=starexx:main"]
    },
    python_requires=">=3.7",
)