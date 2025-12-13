# DIAGNOSE/setup.py

from setuptools import setup, find_packages

setup(
    name="project-diagnose",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "pydantic>=2.0"
    ],
    entry_points={
        "console_scripts": [
            "project-diagnose=project_diagnose.cli:main"
        ]
    },
    author="Razmakh",  # можешь поставить псевдоним
    description="AI-анализатор хаоса проекта и web-интерфейс для просмотра отчётов.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/project-diagnose",  # если будет
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
)
