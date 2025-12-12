from setuptools import setup, find_packages

_requirements = [line.split('#')[0].strip() for line in open("requirements.txt").readlines() if all([line.strip(), not line.startswith("#")])]

setup(
    name="ws_bom_robot_app",
    version="0.0.103",
    description="A FastAPI application serving ws bom/robot/llm platform ai.",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Websolute Spa",
    author_email="dev@websolute.it",
    url="https://github.com/websolutespa/bom",
    packages=find_packages(),
    install_requires=_requirements,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
