from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='vbvstatus',
    version='0.1.0',
    author='@unik_xd',
    author_email='unik_xd@example.com', # Placeholder email
    description='A command-line tool and library for checking VBV status and performing BIN lookups.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/GunYamazakii/vbvstatus-pypi', # Placeholder URL
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    package_data={
        'vbvstatus': ['vbvbin.txt'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vbvstatus=vbvstatus.__init__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
