import os
from typing import List

import setuptools


LIB_NAME = "traceblame"
LIB_VERSION = "0.0.1"


class Setup:
    def setup(self):
        setuptools.setup(
            author="ncopiy",
            author_email="ncopiy@yandex.com",
            long_description=self.get_long_description(),
            long_description_content_type="text/markdown",
            url="https://github.com/ncopiy/traceblame",
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
            ],
            description="Tool to extend locals variables in stacktrace by git blame information for python projects",
            install_requires=self.get_requirements(),
            name=LIB_NAME,
            packages=self._get_package_dir(LIB_NAME),
            version=LIB_VERSION,
        )

    def get_requirements(self) -> List[str]:
        requirements = []

        with open("requirements.txt", "r") as fh:
            req = fh.readlines()
        requirements.extend((r for r in req if r != "\n"))

        return requirements

    def get_long_description(self) -> str:
        with open("README.md", "r") as fh:
            long_description = fh.read()

        return long_description

    def _get_package_dir(self, path) -> List[str]:
        top_level_dirs = os.listdir(path)

        current_paths = [path]

        for p in top_level_dirs:
            if p != "__pycache__":
                full_path = os.path.join(path, p)

                if os.path.isdir(full_path):
                    current_paths.append(full_path)
                    paths = self._get_package_dir(full_path)
                    current_paths.extend(paths)

        return list(set(current_paths))


if __name__ == "__main__":
    parser = Setup()
    parser.setup()
