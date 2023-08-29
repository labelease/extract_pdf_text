from pathlib import Path
from setuptools import find_packages, setup

def read_requirements(path):
    return list(Path(path).read_text().splitlines())

requirements = read_requirements("requirements.txt")

setup(
	name='extract_pdf_text',
	version='0.0.4',
	description='Microservice to extract text from pdf or txt files',
	long_description='Microservice to extract text from pdf or txt files',
	maintainer="labelease, emersonrafaels, naomilago",
    maintainer_email="labeleasecode@gmail.com, emersona7x@hotmail.com",
    license="MIT License",
	py_modules=["extract_pdf_text"],
	packages=find_packages(),
	install_requires=requirements,
	python_requires=">=3.6",
	keywords=["Python", "pdf", "txt"],
)