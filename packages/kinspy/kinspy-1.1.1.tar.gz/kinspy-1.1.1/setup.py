import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme_file = fh.read()

setuptools.setup(
    name="kinspy", 
    version="1.1.1",
    author="Yunxiao Zhang",
    author_email="yunxiao9277@gmail.com",
    description="Make your cmd output colorful in a simply way.",
    long_description=readme_file,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)