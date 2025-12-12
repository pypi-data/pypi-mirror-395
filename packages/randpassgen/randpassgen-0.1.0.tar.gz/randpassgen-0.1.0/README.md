# randpassgen

A simple and customizable random password generator for Python.

## Features
- Choose length
- Enable/disable uppercase, lowercase, digits, and symbols
- Easy and lightweight

## Installation
```python 
pip install randpassgen
```

## Usage
```python
from randpassgen import generate_password

pwd = generate_password(length=16, symbols=True)
print(pwd)
```
