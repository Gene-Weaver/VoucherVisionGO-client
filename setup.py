from setuptools import setup, find_packages

'''
python -m build
python -m twine upload dist/* --verbose
'''

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vouchervision-go-client",
    version="0.1.45",  # "0.1.41" is transition away from client.py
    author="Will",
    author_email="willwe@umich.edu",
    description="Client for VoucherVisionGO API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gene-Weaver/VoucherVisionGO-client",
    project_urls={
        "Bug Tracker": "https://github.com/Gene-Weaver/VoucherVisionGO/issues",
    },
    license="GPL-3.0-only",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # IMPORTANT: include VoucherVision as a top-level module
    py_modules=["VoucherVision", "client", "list_prompts", "url_name_parser"],
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "requests-toolbelt",  # needed for MultipartDecoder
        "termcolor",
        "tabulate",
        "tqdm",
        "pyyaml",   # for list_prompts.py
        "pandas",   # now required; used at import time in VoucherVision.py
        "openpyxl", # needed for pandas to write .xlsx cleanly
    ],
    extras_require={
        "analytics": ["pandas"],
        "full": ["pandas"],
    },
    entry_points={
        "console_scripts": [
            # still point CLI to client:main, which now forwards to VoucherVision.main
            # "vouchervision=client:main",
            "vouchervision=VoucherVision:main",
            "vv-prompts=list_prompts:main",
        ],
    },
)
