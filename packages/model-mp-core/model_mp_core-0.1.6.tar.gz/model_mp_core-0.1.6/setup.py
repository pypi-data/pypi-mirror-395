import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="model-mp-core",
    version="0.1.6",
    author="unihiker Team",
    author_email="unihiker@dfrobot.com",
    description="Core inference library for Mind+ model training tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UNIHIKER/model-pypi-lib",
    project_urls={
        "Bug Tracker": "https://github.com/UNIHIKER/model-pypi-lib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Education"
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        "": ["*.txt", "*.md"],
    },
    install_requires=[
        'numpy>=1.19.0',
        'opencv-python>=4.5.0',
        'pillow>=8.0.0',
        'onnxruntime>=1.8.0',
        'pyyaml>=5.1.0',
        "scikit-learn >=1.7.1",
        "pydantic>=2.12.3",
        "scipy>=1.16.2"
    ],
    python_requires=">=3.7",
)
