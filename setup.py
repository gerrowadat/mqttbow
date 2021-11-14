import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mqttbow",
    version="0.0.1",
    author="Dave O'Connor",
    author_email="doc+git@gerrup.eu",
    url='https://github.com/gerrowadat/mqttbow',
    description="MQTT Publisher/Subscriber for Pimoroni Keybow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    scripts=["mqttbow.py"],
    package_dir={'': '.'},
    keywords=['mqtt', 'keybow'],
    install_requires=['asynckeybow', 'hbmqtt']
)
