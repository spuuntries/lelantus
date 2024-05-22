from setuptools import setup, find_packages

setup(
    name="lelantus",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="An HTML-JPEG polyglot embedder.",
    author="spuun",
    author_email="kek@spuun.art",
    url="https://github.com/spuuntries/lelantus",
    install_requires=["colorama==0.4.6", "minify_html==0.15.0"],
)
