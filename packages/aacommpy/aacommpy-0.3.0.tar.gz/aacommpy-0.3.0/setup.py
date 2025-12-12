import os
from setuptools import setup

about = {
    'name': 'aacommpy',
    'description': 'A Python package for wrapping aacomm nuget package',
    'version': '0.2.4',
    'author': 'HIEU and DB',
    'author_email': 'daniel.brousser@akribis-sys.com',
    'url': 'https://github.com/BoJl4apa/aacommpy',
    'license': 'MIT',
}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'aacommpy', '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['aacommpy'],
    include_package_data=True,
    python_requires=">=3.10.1",
    install_requires=['numpy', 'requests', 'pythonnet'],
    license=about['__license__'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['aacommpy=aacommpy.entry_points:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='package development stage'
)
