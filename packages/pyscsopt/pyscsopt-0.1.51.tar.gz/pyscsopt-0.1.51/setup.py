from setuptools import setup, find_packages

setup(
    name="pyscsopt",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="A Python library for self-concordant smooth optimization (Python port of SelfConcordantSmoothOptimization.jl)",
    author="Adeyemi Damilare Adeoye",
    author_email="",
    url="https://github.com/adeyemiadeoye/pyscsopt",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "jax",
    ],
    python_requires=">=3.8",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)