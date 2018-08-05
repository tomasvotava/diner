# Development Setup
Setup scripts for development usage.

## Requirements
- Python 3
- *pformat* library for Python ([Available on GitHub](https://github.com/tomasvotava/pformat))
- *mysql-connector* for Python ([dev.mysql.com](https://dev.mysql.com/downloads/connector/python/))

## Usage
### Install prerequisites
#### Install pformat
```bash
$ git clone https://github.com/tomasvotava/pformat.git
$ cd pformat
$ ./setup.py install
```

#### Install mysql-connector
```bash
$ python3 -m pip install --upgrade pip
$ python3 -m pip install mysql-connector
```
### Make the script executable
```bash
$ chmod u+x setupdev.py
```
### Run the script
```bash
# ./setupdev.py
```

Follow the instructions in terminal.
