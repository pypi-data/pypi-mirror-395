from setuptools import setup, find_packages
import os

# Safe README read (no crash if missing)
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="soketdb_client",
    version="1.5.0",
    author="Alex Austin",
    author_email="benmap40@gmail.com",
    description=(
        "SoketDB_client — a zero-setup, AI-smart JSON database client built for developers who value speed, simplicity, "
        "cloud-backed persistence — all in one self-contained system."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythos-team/soketdb",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
  #  entry_points={
        #"console_scripts": [
            #"soketdb_client = soketdb:cli_main",  # Points to cli_main() in __init__.py
 #       ],
#    },
    python_requires=">=3.7",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=[
        "database",
        "json",
        "sql",
        "ai",
        "nlp",
        "offline",
        "lightweight",
        "local-storage",
        "cloud-sync",
        "huggingface",
        "google-drive",
    ],
)