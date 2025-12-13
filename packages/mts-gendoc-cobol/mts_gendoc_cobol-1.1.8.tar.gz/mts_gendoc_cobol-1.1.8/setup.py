
from setuptools import setup, find_packages

setup(
    name="mts-gendoc-cobol",
    version="1.1.8",
    description="A set of CLI helpers for COBOL doc generation and file utilities.",
    author="Ben Bastianelli",
    author_email="benbastianelli@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0",
        "Markdown>=3.0",
        "tqdm>=4.0",
    ],
    entry_points={
        'console_scripts': [
            'change=gen_doc.change:main',
            'automate=gen_doc.automate:automate',
            'gendoc=gen_doc.__main__:main',
            'upload=gen_doc.publish:main',
            'pdf = gen_doc.prepare_pdfs:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
