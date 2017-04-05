import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def tests_require():
    required = ['pytest', 'pytest-cov']
    if sys.version_info < (3, 3):
        required.append('mock')
    return required


def install_requires():
    return []


def description():
    return (
        "TODO"
    )


setup(
    name='alembic-stage',
    version='1.0a0',
    description='Alembic plugin to allow operations to staged before execution',
    long_description=description(),
    author='Aubrey Stark-Toller',
    author_email='aubrey@kleetope.uk',
    license='GPL3',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=['alembic_stage'],
    install_requires=install_requires(),
    tests_require=tests_require(),
    cmdclass={'test':PyTest},
)
