from distutils.core import setup

setup(
    name="nova_api",
    version="0.1.0",
    author="Chaps",
    author_email="drumchaps@gmail.com",
    maintainer="Chaps",
    maintainer_email="drumchaps@gmail.com",
    url="https://github.com/chaps/nova_api",
    packages=[
        "nova_api",
    ],
    package_dir={'': 'src'},
    install_requires=["requests", ]
)
