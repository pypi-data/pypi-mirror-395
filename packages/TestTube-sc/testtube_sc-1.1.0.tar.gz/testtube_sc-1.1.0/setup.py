from setuptools import setup, find_packages

setup(
    name="TestTube-sc",
    version="1.1.0",
    author="SpaceCat",
    author_email="unavailab@notarealemail.com",
    description="Websites built fast.",
    long_description="TestTube is a lightweight Python back-end platform that lets Python users add dynamic, interactive web pages without needing to write JavaScript. ",
    url="https://github.com/spacecat031/TestTube",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    options={'bdist_wheel': {'universal': True}},
)
