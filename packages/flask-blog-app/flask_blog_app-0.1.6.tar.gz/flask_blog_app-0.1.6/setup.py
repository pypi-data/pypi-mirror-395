from setuptools import setup, find_packages

setup(
    name='flask-blog-app',
    version='0.1.6',
    description='A simple Flask blog application.',
    author='Gruppo I Processati',
    py_modules=['app', 'data'], 
    
    packages=find_packages(),
    install_requires=[
        'Flask',
        'flask-mysqldb',
        'WTForms',
        'passlib',
        'gunicorn',
    ],
    include_package_data=True, 
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Flask',
    ],
    python_requires='>=3.11',
)