from pathlib import Path

from setuptools import find_packages, setup


def read_requirements() -> list[str]:
    req_file = Path(__file__).parent / "requirements.txt"
    if req_file.exists():
        return [line.strip() for line in req_file.read_text().splitlines() if line.strip() and not line.startswith("#")]
    return []


setup(
    name="jumpyng",
    version="0.1.9",
    description="Utilities for processing DeepLabCut jumping experiments",
    author="Kevin",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={"dlc": ["deeplabcut"]},
    python_requires=">=3.9",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
