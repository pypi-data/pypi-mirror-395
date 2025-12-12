from setuptools import setup, find_packages

setup(
    name="ai_text_ap",          # must be unique on PyPI; lowercase
    version="0.1.0",
    description="Simple AI text helpers (example) - ai_text_ap",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Anaswara",
    license="MIT",                    # <-- ADD THIS
    license_files=["LICENSE"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
