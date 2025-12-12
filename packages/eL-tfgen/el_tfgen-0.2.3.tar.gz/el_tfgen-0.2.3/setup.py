from setuptools import setup, find_packages

setup(
    name="eL-tfgen",
    version="0.2.3",
    description="Generate Terraform modules from documentation using AI",
    author="eLTitans",
    packages=find_packages(exclude=['tfgen_original', 'tfgen_original.*', 'tfgen_obf', 'tfgen_obf.*']),
    package_data={
        'tfgen': [
            'pyarmor_runtime_000000/*.py',
            'pyarmor_runtime_000000/*.pyd',
            'pyarmor_runtime_000000/*.so',
            'pyarmor_runtime_000000/*.dll',
        ],
    },
    include_package_data=True,
    install_requires=[
        "playwright",
        "beautifulsoup4",
        "anthropic",
        "python-dotenv",
        "Pillow",
        "customtkinter",
    ],
    entry_points={
        "console_scripts": [
            "tfgen=tfgen.cli:cli",
            "tfgen-ui=tfgen.ui:main",
        ],
    },
    python_requires=">=3.8",
)