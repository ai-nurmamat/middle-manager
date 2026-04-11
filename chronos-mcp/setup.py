from setuptools import setup, find_packages

setup(
    name="chronos-mcp",
    version="0.1.0",
    description="A disruptive Universal 4D Hypergraph (S-P-O-T) memory engine for LLMs.",
    author="Chronos Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.0.0",
        "openai>=1.0.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
