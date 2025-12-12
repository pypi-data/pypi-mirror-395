# cputils

[![license MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)

Utilities for Competitive Programming. 

Features:
- Download samples from [kattis](https://open.kattis.com/), [aceptaelreto](https://aceptaelreto.com/), [adventofcode](https://adventofcode.com/).
- Test in c, cpp, python, java, rust, ruby, bash, nim.
- Submit to kattis.
- Interactive CLI menu.

Tests only for complete textual match, ignoring leading and trailing whistespaces. 

## Installation
Assuming you have a [Python3](https://www.python.org/) distribution with [pip](https://pip.pypa.io/en/stable/installing/), install the package running:

```bash
pip3 install cputils
```

## Usage
Typically you'll want to work on a dedicated repo/folder for your task (solving the problems in a server, preparing problems...).
You should first create a configuration file defining how cputils will work on that repo/folder and then use the CLI or the commands to work in it.

### cpconfig
To create a config file, run
```bash
cpconfig
```

### cpsamples
To download the samples of a problem run
```bash
cpsamples <problem>
```

### cptest
To test a solution or set of solutions run
```bash
cptest <problem>/<solution(s)>
```
Pro-tip: you can use glob patterns like ```problem/code*``` or ```problem/*.py```.

### cpsubmit
To submit a solution (only kattis)
```bash
cpsubmit <problem>/<solution(s)>
```

### cpmenu
To run an interactive CLI
```bash
cpmenu
```

Yo can also provide the problem and language with the arguments, or change it in the menu. See help (h) for more info.


## Development
### Testing

Testing requires installing the test extra. Furthermore, some tests require the languages to be installed and available.

To run all tests:
```bash
make test
```

To run a single test module:
```bash
pytest tests/test_<test_name>.py
```