from setuptools import setup

setup(
    name = 'ejercicio13-efm',
    py_modules = ['operaciones'],
    version = '0.2a',
    license='MIT',
    description = 'Libreria de mates',
    author = 'Erika Fernández Moreno',
    author_email = 'erika@edrakon.tech',
    keywords = ['mates', 'suma', 'resta', 'multiplicacion', 'division'],
    install_requires=[
            'pytest',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.14'
    ],
    python_requires='>=3.14',
)