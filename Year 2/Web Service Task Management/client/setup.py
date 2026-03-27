from setuptools import setup, find_packages

setup(
    name='task_manager_library',
    version='1.0.0',
    author='Bernacchia and Fernandez',
    author_email='sergio.fernandezdiz@supsi.ch,alessia.bernacchia@supsi.ch',
    description='Library package for task_manager applications',
    packages=find_packages(),
    install_requires=["requests","plotly","pandas","matplotlib"]
)