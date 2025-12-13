from setuptools import setup, find_packages
 
setup(
    name='Permanent_variable_tool',
    version='1.0.5',
    packages=find_packages(),
    author='Unwilling to disclose',
    author_email='q1111911111q@outlook.com', 
    description='Used to store variables permanently, which can be read directly after importing into the library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    keywords='Permanent variable tool',
)