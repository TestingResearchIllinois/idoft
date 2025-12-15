from setuptools import setup

setup(
    name="auto-update-dataset",
    version="0.0.1",
    description="Utility for parallel checking of GitHub repositories for archived status using data files.",
    readme="README.md",
    install_requires=[
        'pandas',
        'requests-html[html_clean]',
        'lxml_html_clean'
    ],
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'auto-update-dataset=repoArchivedCheck:main'
        ]
    },
    py_modules=['repoArchivedCheck']
)
