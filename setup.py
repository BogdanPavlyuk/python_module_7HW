from setuptools import setup, find_namespace_packages

setup(
    name='CleanFolder_BogdanPavlyuk',
    version='0.0.6',
    description='Clean Folder file sorter by Python',
    author='Bogdan Pavlyuk',
    author_email='bodjapavljuk@gmail.com',
    url='https://github.com/BogdanPavlyuk',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:file_parser']})
