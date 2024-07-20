from setuptools import setup, find_packages

setup(
    name='storify',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A short project description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Author Name',
    author_email='author@example.com',
    url='https://github.com/benbaptist/storify',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        # List your package dependencies here
    ],
)