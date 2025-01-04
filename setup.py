from setuptools import setup, find_packages

setup(
    name="rofi-vim",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "rofi", 
        "fzf"
    ],
    entry_points={
        'console_scripts': [
            'fzf-vim=rofi_vim.fzf:main',
            'rofi-vim=rofi_vim.rofi:main',
        ],
    },
    package_data={
        'rofi_vim': ['db/*.json', 'icon.png'],
    },
    author="Ubuntpunk",
    author_email="ubuntupunk@gmail.com",
    description="A Vim cheatsheet browser using rofi/fzf",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/rofi-vim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)