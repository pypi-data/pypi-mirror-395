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

#######################################################################
# Targets
#######################################################################

all:

clean:
	-$(RMDIR) __pycache__

.PHONY: all clean
