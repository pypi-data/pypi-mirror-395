from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="corva-worker-python",
    author="Jordan Ambra <jordan.ambra@corva.ai>, Mohammadreza Kamyab <m.kamyab@corva.ai>",
    url="https://github.com/corva-ai/corva-worker-python",
    version="2.2.2",
    classifiers=classifiers,
    python_requires=">=3.13",
    description="SDK for interacting with Corva",
    keywords="corva, worker",
    packages=find_packages(exclude=["testcase"]),
    install_requires=[
        "numpy>=2.3.5",
        "redis>=5.2.1",
        "requests>=2.32.5",
        "simplejson>=3.20.2",
        "urllib3>=2.5.0",
    ],
    include_package_data=True,
    license="Unlicensed",
)
