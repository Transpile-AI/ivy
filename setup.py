# lint as: python3
# Copyright 2021 The Ivy Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License..
# ==============================================================================
__version__ = None

import setuptools
from setuptools import setup
from pathlib import Path
from packaging import tags
import os
import json
import requests
import itertools
import re
from tqdm import tqdm


def _get_paths(binaries, root_dir=""):
    paths = []
    if isinstance(binaries, str):
        return [os.path.join(root_dir, binaries)]
    elif isinstance(binaries, dict):
        for k, v in binaries.items():
            paths += _get_paths(v, os.path.join(root_dir, k))
    else:
        for i in binaries:
            paths += _get_paths(i, root_dir)
    return paths


def _strip(line):
    return line.split(" ")[0].split("#")[0].split(",")[0]


# Download all relevant binaries in binaries.json
all_tags = list(tags.sys_tags())
binaries = json.load(open("binaries.json"))
paths = _get_paths(binaries)
terminate = False
pbar = None
spinner = itertools.cycle(["-", "\\", "|", "/"])
version = os.environ["VERSION"] if "VERSION" in os.environ else "main"
print(f"Locating binaries {next(spinner)} ", end="")

for tag in all_tags:
    print(f"\rLocating binaries {next(spinner)} ", end="")
    if terminate:
        pbar.close()
        break
    for i, path in enumerate(paths):
        if os.path.exists(path):
            continue
        folders = path.split(os.sep)
        folder_path, file_path = os.sep.join(folders[:-1]), folders[-1]
        file_name = f"{file_path[:-3]}_{tag}.so"
        search_path = f"compiler/{file_name}"
        r = requests.get(
            f"https://github.com/unifyai/binaries/raw/{version}/{search_path}",
            timeout=40,
        )
        if r.status_code == 200:
            if pbar is None:
                print()
                print("Downloading binaries ...")
                pbar = tqdm(total=len(paths))
            with open(path, "wb") as f:
                f.write(r.content)
            terminate = path == paths[-1]
            pbar.update(1)
        else:
            break


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Remove img tags that have class "only-dark"
long_description = re.sub(
    r"<img [^>]*class=\"only-dark\"[^>]*>",
    "",
    long_description,
    flags=re.MULTILINE,
)

# Remove a tags that have class "only-dark"
long_description = re.sub(
    r"<a [^>]*class=\"only-dark\"[^>]*>((?:(?!<\/a>).)|\s)*<\/a>\n",
    "",
    long_description,
    flags=re.MULTILINE,
)

# Apply version
with open("ivy/_version.py") as f:
    exec(f.read(), __version__)

setup(
    name="ivy",
    version=__version__,
    author="Unify",
    author_email="hello@unify.ai",
    description=(
        "The unified machine learning framework, enabling framework-agnostic "
        "functions, layers and libraries."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://unify.ai/ivy",
    project_urls={
        "Docs": "https://unify.ai/docs/ivy/",
        "Source": "https://github.com/unifyai/ivy",
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        _strip(line)
        for line in open("requirements/requirements.txt", "r", encoding="utf-8")
    ],
    classifiers=["License :: OSI Approved :: Apache Software License"],
    license="Apache 2.0",
)
