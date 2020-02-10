from setuptools import setup, find_packages

DEPENDENCIES = ["fire", "requests"]
TEST_DEPENDENCIES = ["pillow", "pylint", "pytest", "responses"]

setup(
    name="pi-camera-capture",
    version="0.1.1",
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": ["pi-camera-capture=pi_camera_capture.cli:cli"]
    },
    install_requires=DEPENDENCIES,
    test_require=TEST_DEPENDENCIES,
    extras_require={"test": TEST_DEPENDENCIES},
)
