from setuptools import setup, find_packages
import os
pjoin = os.path.join
repo_root = os.path.dirname(os.path.abspath(__file__))

try:
    # make this optional, but it's better for PyPI uploads
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")
except:
    print("!!! DON'T UPLOAD TO PyPI, DESCRIPTION IS WRONG FORMAT")
    import io
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

setup(
    name='watermark',
    version='1.2.3',
    license='newBSD',
    description=('IPython magic function to print date/time stamps and'
                 'various system information.'),
    long_description=long_description,
    author='Sebastian Raschka',
    author_email='mail@sebastianraschka.com',
    url='https://github.com/rasbt/watermark',
    packages=find_packages(exclude=[]),
    install_requires=['ipython']
)
