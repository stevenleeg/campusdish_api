from pip.req import parse_requirements
from distutils.core import setup

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="campusdish_api",
    version="0.1",
    url="http://github.com/stevenleeg/campusdish_api",
    license="MIT",
    author="Steve Gattuso",
    author_email="steve@stevegattuso.me",
    description="A scraper-based API for the University of Rochester's dining services",
    install_requires=reqs,
    packages=["campusdish_scraper", "campusdish_api"],
    scripts=["bin/cd_api"]
)
