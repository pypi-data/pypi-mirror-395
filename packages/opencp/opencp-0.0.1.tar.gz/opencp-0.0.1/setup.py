from setuptools import setup, Extension, find_packages

# Define the C extension
queue_module = Extension(
    "opencp.backend.c_queue",  # The full python path to the module
    sources=["src/opencp/backend/c_queue.c"],  # Where the C file is located
)

setup(
    name="opencp",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[queue_module],  # Add the C extension here
)
