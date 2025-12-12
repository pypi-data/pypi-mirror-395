from setuptools import setup, find_packages

setup(
    name='stmath',
    version='1.0.9',
    author='Saksham Tomar',
    description='The Next-Generation Unified Math + AI + ML + Quantum Engine',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='math ai ml quantum crypto optimization vision stmath',
)
