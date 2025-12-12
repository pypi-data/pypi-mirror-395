from setuptools import setup, find_packages

setup(
    name='attractor-tools',
    version='0.2.0',
    author='Silas Schimpeler',
    author_email='silasfelix2005@gmail.com',
    description='animate simon attractors',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/beasty79/attractor_api',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
