from setuptools import setup, find_packages

setup(
    name="n8nControl",
    version="1.7.0",
    author="LEV",
    author_email="you@example.com",
    description="Python agent to control remote n8n instances",
    packages=find_packages(include=['n8nControl', 'n8nControl.*']),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "n8nagent = n8nControl.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)