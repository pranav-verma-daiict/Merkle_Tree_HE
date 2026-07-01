from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="merkle-tree-he",
    version="0.1.0",
    author="Pranav Verma",
    author_email="pranav@example.com",
    description="Merkle Tree with Homomorphic Encryption for zero-knowledge membership proofs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pranav-verma-daiict/Merkle_Tree_HE",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    keywords="merkle-tree homomorphic-encryption zero-knowledge-proofs cryptography",
)
