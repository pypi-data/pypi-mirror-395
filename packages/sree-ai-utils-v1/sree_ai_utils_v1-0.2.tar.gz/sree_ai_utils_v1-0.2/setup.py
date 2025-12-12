from setuptools import setup, find_packages

setup(
    name="sree_ai_utils_v1",  
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'google-generativeai', 
        'flask'
    ],
    author="Sreeraj",
    description="A simple AI helper library for Project 3",
)