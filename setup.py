from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Charge app that connects wallbox and photovoltaics'
LONG_DESCRIPTION = 'Can calculate current current surplus and set target current correspondingly'

# Setting up
setup(
    name="heidelbergChargeApp",
    version=VERSION,
    author="Kerstin Baskakow",
    author_email="<kerstin.baskakow@web.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python','heidelberg','charger','smarthome'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)