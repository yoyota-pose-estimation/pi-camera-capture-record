from setuptools import setup, find_packages

required_packages = ["pillow", "pylint", "pytest", "requests"]

setup(
    name="pi_camera_capture",
    install_requires=required_packages,
    packages=find_packages(),
)
