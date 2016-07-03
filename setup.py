from setuptools import setup, find_packages

setup(
    name="ultimate-tic-tac-toe",
    version="0.1",
    packages=find_packages(),
    install_requires=['PyQt5>=5.6'],
    test_suite='tests',
    author="Svetomir Stoimenov",
    description="The Ultimate Tic-Tac-Toe game",
    license="MIT",
    keywords="ultimate tic-tac-toe",
)
