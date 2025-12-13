from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

readme = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else ""

setup(
    name="plumbking",
    version="0.1.0",
    description="Classical CV-based image leveling and thumbnail generator.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="",
    url="https://github.com/your-user/plumbking",  # update or remove if you want
    license="AGPL-3.0-or-later",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.22",
        "opencv-python>=4.8",
        "Pillow>=9.0",
        "scikit-learn==1.7.*"
    ],
    entry_points={
        "console_scripts": [
            # `plumbking -d /path` on the CLI
            "plumbking=plumb.king.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    include_package_data=True,
    zip_safe=False,
)
