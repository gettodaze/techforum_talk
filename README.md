# techforum_webscraping

### Setup:

- (intended for python 3.8)
- Download and unzip files from https://www.kaggle.com/crawford/cat-dataset into a subdirectory "input", removing the "cats" directory (it is a duplicated version of the main folder)
- create a new virtual-env. example: `python -m venv ~/.env-tf_webscraping` and activate (`. ~/.env-tf_webscraping/bin/activate`).
- pip install -r requirements.txt
- from the repository, run `pwd > ~/.env-tf_webscraping/lib/python3.8/site-packages/tf_webscraping.pth` (Now in IPython, when running `import sys; sys.path`, the repository directory should appear.)
