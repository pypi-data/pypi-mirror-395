from setuptools import setup

setup(
    name="evil-rce2",
    version="1.0.0",
    author="Security Researcher",
    description="RCE reverse shell script",
    py_modules=["rce"],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "evil-rce2=rce:main",
        ],
    },
)
