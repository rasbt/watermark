import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="watermark",
    version="1.2.2",
    author="Sebastian Raschka",
    author_email="mail@sebastianraschka.com",
    description=("An IPython magic extension for printing date and time"
                   " stamps, version numbers, and hardware information"),
    license="GPL3",
    keywords="ipython jupyter watermark benchmark",
    url="https://github.com/rasbt/watermark",
    modules=['watermark'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL3 License",
    ],
)
