from setuptools import setup

__VERSION__ = ' 9.2.2'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="pyarmor.cli",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version=__VERSION__,
    description="A comand line tool to obfuscate python scripts",
    long_description=long_description,

    license='Free To Use But Restricted',

    url="https://github.com/dashingsoft/pyarmor",
    author="Jondy Zhao",
    author_email="pyarmor@163.com",

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        # Pick your license as you wish
        "License :: Free To Use But Restricted",

        # Support platforms
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Topic :: Security",
        "Topic :: System :: Software Distribution",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="protect obfuscate encrypt obfuscation distribute",

    packages=["pyarmor.cli"],
    package_dir={"pyarmor.cli": "pyarmor/cli"},
    package_data={"pyarmor.cli": ["default.cfg", "public_capsule.zip", "core.data.*"]},

    install_requires=[
        'pyarmor.cli.core~=8.1.0'
    ],

    entry_points={
        'console_scripts': [
            'pyarmor=pyarmor.cli.__main__:main',
            'pyarmor-auth=pyarmor.cli.docker:main',
        ],
    },

)
