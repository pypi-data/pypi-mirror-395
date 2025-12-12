from pathlib import Path
from setuptools import setup, find_namespace_packages

BASE_DIR = Path(__file__).parent

def read_readme() -> str:
    readme_file = BASE_DIR / "README.md"
    if readme_file.exists():
        return readme_file.read_text(encoding="utf-8")
    return "SDK для получения списка участников Telegram-чата через HTTP-эндпоинт."

setup(
    name="dlab-tg-sso",
    version="0.1.0",
    description="SDK для получения списка участников Telegram-чата",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="",
    license="MIT",
    packages=find_namespace_packages(include=["dlab*"]),
    include_package_data=True,
    install_requires=[
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
)


