from setuptools import setup, find_packages

setup(
    name="libdqp",
    version="0.1.0",
    description="Differentiation Through Black-Box Quadratic Programming Solvers",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    license_files=('LICENSE'),

    author=[
        "Connor W. Magoon",
        "Fengyu Yang",
        "Noam Aigerman",
        "Shahar Z. Kovalsky",
    ],
    keywords=[
        "quadratic programming",
        "differentiation",
        "optimization",
        "pytorch",
        "machine learning",
    ],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],

    packages=find_packages(where="."),
    include_package_data=True,

    install_requires=[
        "torch>=2.0.0",
        "numpy",
        "scipy",
        "qpsolvers",
        "joblib",

        "clarabel",
        "cvxopt",
        "daqp",
        "ecos",
        "gurobipy",
        "highspy",
        "mosek",
        "osqp",
        "piqp",
        "proxsuite",
        "qpalm",
        "quadprog",
        "scs",

        "pypardiso",
        "qdldl",
    ],

    project_urls={
        "Homepage": "https://github.com/cwmagoon/dQP",
        "Paper": "https://arxiv.org/pdf/2410.06324",
    },

    package_data={
        "": ["*.npz", "*.txt"],
    },
)