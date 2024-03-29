# setup.py

import codecs

with codecs.open('build.py', 'r') as build_file:
    build_source = build_file.read()

source = dict()

exec(build_source, source)

setup = source['setup']

def main() -> None:
    """Runs the function to distribute the package."""

    setup(
        package="looperation",
        exclude=[
            "__pycache__",
            "*.pyc"
        ],
        include=[],
        requirements="requirements.txt",
        dev_requirements="requirements-dev.txt",
        name='looperation',
        version='2.0.0',
        description=(
            "A python module to easily run loop based operations, "
            "control the starting, stopping of the loop, "
            "and handle exceptions in real time."
        ),
        license='MIT',
        author="Shahaf Frank-Shapir",
        author_email='shahaffrs@gmail.com',
        url='https://github.com/Shahaf-F-S/looperation',
        long_description_content_type="text/markdown",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Operating System :: OS Independent"
        ]
    )

if __name__ == "__main__":
    main()
