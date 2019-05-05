# MNIST Classifier

Requires python v3

## Instructions
- Create a python venv and activate  
```bash
$ python -m venv testEnvironment
$ cd testEnvironment
$ ./Scripts/activate
```
- Clone this repository into the venv
```bash
$ git clone https://github.com/faztp12/mnist_digit_recognizer.git
```
- Install this on the virtual env
```bash
$ pip install -e ./mnist_digit_recognizer
```
- Train the models, optionally
```bash
$ python -m mnist_digit_recognizer
$ python -m mnist_digit_recognizer.conv # for conv network
```
- Start the GUI
```bash
$ python -m mnist_digit_recognizer.gui
```