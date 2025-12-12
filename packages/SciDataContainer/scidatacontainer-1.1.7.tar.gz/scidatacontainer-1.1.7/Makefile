# Makefile for the Python implementation of SciDataContainer

#######################################################################
# Common variable definitions
#######################################################################

ifeq ($(OS),Windows_NT)
    RMDIR := rmdir /s /q
	RM := del /q
else
    RMDIR := rm -rf
	RM := rm -f
endif

MAKE := make
PYTHON := python
COVERAGE := coverage

#######################################################################
# Targets
#######################################################################

install: bdist
	$(PYTHON) -m pip install .

clean:
	-$(RMDIR) build
	-$(RMDIR) dist
	-$(RMDIR) SciDataContainer.egg-info
	-$(RM) VERSION
	$(MAKE) -C scidatacontainer clean
	$(MAKE) -C test clean

sdist: clean
	$(PYTHON) setup.py sdist

bdist: clean
	$(PYTHON) setup.py bdist_wheel

pypi:
	$(PYTHON) -m twine upload dist/*

test:
	$(PYTHON) -m unittest discover

coverage:
	$(COVERAGE) run -m unittest discover

report: coverage
	$(COVERAGE) report -i

htmlreport: coverage
	 $(COVERAGE) html -i

all: install pypi

.PHONY: clean test sdist bdist install pypi all
