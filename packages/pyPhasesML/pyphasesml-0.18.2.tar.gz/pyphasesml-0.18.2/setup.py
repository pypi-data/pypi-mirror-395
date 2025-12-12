import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyPhasesML",
    version="v0.18.2"[1:],
    author="Franz Ehrlich",
    author_email="fehrlichd@gmail.com",
    description="A Framework for creating a boilerplate template for ai projects that are ready for MLOps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tud.ibmt.public/pyphases/pyphasesml/",
    packages=setuptools.find_packages(),
    package_data={"": ["*.yaml"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyPhases", "typeguard"],
    python_requires=">=3.5",
)
