from setuptools import setup, find_packages

try:
    import setuptools_scm
    use_scm_version = True
except ImportError:
    use_scm_version = False

if use_scm_version:
    version = setuptools_scm.get_version()
else:
    version = "0.1"
    
setup(
    name="taksa",
    version=version,
    packages=find_packages(),
    install_requires=[

    ],
    author="Eugene Dombrovsky",
    author_email="e.prog.d@gmail.com",
    description="Dependency manager for C++",
    url="https://github.com/eProgD/taksa.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
