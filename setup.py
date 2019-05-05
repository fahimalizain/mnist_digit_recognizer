from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
    name='mnist_digit_recognizer',
    version='0.1.0',
    description='MNIST Dataset Classifier',
    long_description=readme,
    author='Fahim Ali Zain',
    author_email='faztp12@github.com',
    install_requires=install_requires,
    url='https://github.com/faztp12/mnist_digit_recognizer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)