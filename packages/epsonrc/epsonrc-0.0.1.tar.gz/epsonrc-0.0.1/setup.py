from setuptools import setup, find_packages

setup(
    name='epsonrc',  # Nota: cambié 'esponrc' a 'epsonrc' para que coincida con tu módulo
    version='0.0.1',
    description='EPSON RC Library for Python',
    long_description=open('USAGE.md', encoding='utf-8').read(),  # ← AQUÍ está el cambio
    long_description_content_type='text/markdown',
    author='David Rosales',
    author_email='daparohe@gmail.com',
    packages=find_packages(),
    install_requires=[
        # pytest no debería estar aquí, es una dependencia de desarrollo
    ],
    extras_require={
        'dev': ['pytest']  # Mejor ponerlo aquí
    },
    license='MIT',
    python_requires='>=3.7',
)