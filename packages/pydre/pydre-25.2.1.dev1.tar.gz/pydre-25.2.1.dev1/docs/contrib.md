# Contributing

Thank you for contributing to `pydre`! 

If you have suggestions or bug reports, please open an issue. If you want to contribute new features, please make a pull request.

The [GitHub "Issues" tab](https://github.com/OSUDSL/pydre/issues) can be used to track bugs and feature requests. 

## Bug reports
Bug reports from users are important for identifying unintentional behavior. If you find a bug, please open a new issue with the following:

1. An explanation of the problem with enough details for others to reproduce the problem. Some  common information needed is:
    * Operating system
    * Python version
    * Any commands executed (perhaps a python snippet)
    * An error message from the terminal
2. An explanation of the expected behavior. For example:
    * I ran `numpy.add(1,2)` which gave me an output of `-999`, but I expected `3`. 


## Development Environment
In order to add new features to `pydre` you need to set up a working development environment.
First, you must create a [fork](https://github.com/OSUDSL/pydre/fork) on your local github account. Then use the following 
commands. 

```bash
# 1. Clone your fork
git clone https://github.com/<your_username>/pydre.git
# 2. Enter the pydre directory
cd pydre
# 3. switch to the development branch
git switch develop
git remote add OSUDSL https://github.com/OSUDSL/pydre.git  # the official repository
git pull OSUDSL  # pull down the up-to-date development version of pydre
rye sync
rye run pytest  # make sure all tests pass
```

## Making a pull request
A good pull request requires the following, along with a new feature (where applicable)

1. All functions should have docstrings using the [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
2. Ideally, new functions should have corresponding unit tests.
3. All tests must pass on your machine by running `rye run pytest` in the top level directory.
4. All new features must be appropriately documented.
5. Code should follow [PEP8 style](http://www.python.org/dev/peps/pep-0008/). 