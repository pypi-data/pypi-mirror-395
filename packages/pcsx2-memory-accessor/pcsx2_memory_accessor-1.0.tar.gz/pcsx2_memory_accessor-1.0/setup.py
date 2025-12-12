import setuptools

# This block reads the content of your README.md file
# and assigns it to the long_description variable.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pcsx2-memory-accessor', 
    # Version must be incremented to upload changes to PyPI/TestPyPI
    version='1.0', 
    packages=setuptools.find_packages(),
    package_data={
        # Package data needs the underscore name
        'pcsx2_memory_accessor': ['dll/*.dll', 'dll/*.so'],
    },
    include_package_data=True, 
    
    # Short description
    description='A Python API for reading & writing PCSX2\'s emulator memory, using the Pine IPC protocol.',
    
    # This is the crucial part that uses the README.md content
    long_description=long_description,
    long_description_content_type="text/markdown", 
    
    author='Composer',
    url='https://github.com/C0mposer/PCSX2-Memory-Accessor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
)