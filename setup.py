from setuptools import setup, find_packages

setup(
    name="vim-prompt",
    version="0.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
    entry_points={
    'console_scripts': [
            'fzf-vim=vim_prompt.fzf:main',
            'rofi-vim=vim_prompt.rofi:main',
        ],
    },
    package_data={
        'vim_prompt': ['db/*.json', 'icon.png'],
    },
    author="Ubuntpunk",
    author_email="ubuntupunk@gmail.com",
    description="A Vim cheatsheet prompter and command browser using rofi/fzf",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/vim-prompt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)