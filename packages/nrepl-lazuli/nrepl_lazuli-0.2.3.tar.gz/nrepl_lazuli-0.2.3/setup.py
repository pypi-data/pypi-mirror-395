from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
#
setup(
    name="nrepl-lazuli",
    version="0.2.3",
    author="Maurício Szabo",
    author_email="mauricio@szabo.link",
    description="A nREPL server to be used with the Lazuli project",
    long_description="A nREPL server to be used with the Lazuli project",
    # long_description_content_type="text/markdown",
    url="https://gitlab.com/clj-editors/nrepl-lazuli-python",
    packages=find_packages(),
    install_requires=[ ],
    extras_require={ },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
