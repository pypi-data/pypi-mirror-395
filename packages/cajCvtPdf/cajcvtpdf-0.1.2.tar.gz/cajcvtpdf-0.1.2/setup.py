from pathlib import Path

from setuptools import find_packages, setup


HERE = Path(__file__).parent
README_PATH = HERE / "README.md"
if README_PATH.exists():
    LONG_DESCRIPTION = README_PATH.read_text(encoding="utf-8")
else:
    LONG_DESCRIPTION = ""


setup(
    name="cajCvtPdf",
    version="0.1.2",
    description="A caj2pdf tool",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Null Name",
    author_email="email@example.com",
    url="https://github.com/caj2pdf/caj2pdf",
    packages=find_packages(),
    package_data={
        "cajCvtPdf": ["bin/*.exe", "bin/*.dll"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "caj2pdf=cajCvtPdf.cli:main",
        ],
    },
    zip_safe=False,
)
