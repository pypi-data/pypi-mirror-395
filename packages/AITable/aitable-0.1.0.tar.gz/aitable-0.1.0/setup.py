from setuptools import setup, find_packages

setup(
    name="AITable",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "datascience>=0.12.2",
        "gradio_client>=0.2.10"
    ],
    python_requires=">=3.9",
    description="Summarize any CSV using ACC AI with predictions and stylized summaries",
    author="Tej Andrews",
    author_email="tej.andrews@gmail.com",
    url="https://github.com/ACC-AGI/AITable",
    license="MIT",
)
