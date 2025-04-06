from setuptools import setup, find_packages

setup(
    name="music-renamer",
    version="1.0.0",
    description="Herramienta para renombrar y gestionar metadatos de archivos de música",
    author="cosLatte",
    author_email="gabrielpazruiz02@gmail.com",
    maintainer="Sataros221",
    maintainer_email="sataros221@gmail.com",
    packages=find_packages(),
    install_requires=[
        "mutagen",
        "requests",
        "syncedlyrics",
        "pyacoustid",
    ],
    entry_points={
        "console_scripts": [
            "music-renamer=music_renamer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
