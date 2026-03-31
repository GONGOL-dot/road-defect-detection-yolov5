#!/usr/bin/env python

import os
import sys
from shutil import rmtree
from sys import platform as _platform

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
NAME = "labelImg"
REQUIRES_PYTHON = ">=3.0.0"
REQUIRED_DEP = ["pyqt5", "lxml"]
about = {}

with open(os.path.join(here, "libs", "__init__.py")) as f:
    exec(f.read(), about)

with open("README.rst", "rb") as readme_file:
    readme = readme_file.read().decode("UTF-8")

with open("HISTORY.rst", "rb") as history_file:
    history = history_file.read().decode("UTF-8")

# OS specific settings
SET_REQUIRES = []
if _platform == "linux" or _platform == "linux2":
    # linux
    print("linux")
elif _platform == "darwin":
    # MAC OS X
    SET_REQUIRES.append("py2app")

required_packages = find_packages()
required_packages.append("labelImg")

APP = [NAME + ".py"]
OPTIONS = {"argv_emulation": True, "iconfile": "resources/icons/app.icns"}


class UploadCommand(Command):
    """Support setup.py upload."""

    description = (readme + "\n\n" + history,)

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print(f"\033[1m{s}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            self.status("Fail to remove previous builds..")
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag -d v{}".format(about["__version__"]))
        os.system("git tag v{}".format(about["__version__"]))
        # os.system('git push --tags')

        sys.exit()


setup(
    app=APP,
    name=NAME,
    version=about["__version__"],
    description="LabelImg is a graphical image annotation tool and label object bounding boxes in images",
    long_description=readme + "\n\n" + history,
    author="TzuTa Lin",
    author_email="tzu.ta.lin@gmail.com",
    url="https://github.com/tzutalin/labelImg",
    python_requires=REQUIRES_PYTHON,
    package_dir={"labelImg": "."},
    packages=required_packages,
    entry_points={"console_scripts": ["labelImg=labelImg.labelImg:main"]},
    include_package_data=True,
    install_requires=REQUIRED_DEP,
    license="MIT license",
    zip_safe=False,
    keywords="labelImg labelTool development annotation deeplearning",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    package_data={"data/predefined_classes.txt": ["data/predefined_classes.txt"]},
    options={"py2app": OPTIONS},
    setup_requires=SET_REQUIRES,
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
