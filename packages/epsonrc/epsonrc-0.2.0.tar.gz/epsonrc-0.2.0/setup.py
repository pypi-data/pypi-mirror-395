from setuptools import setup, find_packages

setup(
    name='epsonrc',
    version='0.0.1',
    description='EPSON RC Library for Python',
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',
    author='David Rosales',
    author_email='daparohe@gmail.com',
    packages=find_packages(),
    install_requires=[
    ],
    extras_require={
        'dev': ['pytest']
    },
    license='MIT',
    python_requires='>=3.7',
)