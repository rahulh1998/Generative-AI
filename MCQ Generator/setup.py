from setuptools import find_packages,setup

setup(
    name = "mcq_generator",
    version="0.0.1",
    author="Rahul Hirondi",
    author_email="rahul.h1998@gmail.com",
    install_requires =['langchain','OpenAI','PyPDF2',"python-dotenv","streamlit"],
    packages=find_packages() 
)