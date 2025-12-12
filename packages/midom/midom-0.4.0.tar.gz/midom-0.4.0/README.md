# MIDOM - Medical Image Deidentification Object Model

[![CI](https://github.com/ResearchBureau/midom/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/ResearchBureau/midom/actions/workflows/build.yml?query=branch%3Amain)
[![PyPI](https://img.shields.io/pypi/v/midom)](https://pypi.org/project/midom/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/midom)](https://pypi.org/project/midom)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A set of concepts and relations to describe the process of DICOM deidentification
and a structured format for a deidentification protocol.


## Why?
For projects related to DICOM deidentification, I'm running into the problem of not 
having the right words. I keep inventing terms, coming up with long-winded descriptions
There is a lack of conceptual clarity. Lack of clarity causes:
* misunderstandings
* Ineffective communication
* misguided programming efforts
* wasted time generally.

The DICOM standard does not have enough detail. 
[DICOM PS3 E-E1](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_E.html#sect_E.1)  gives 
thorough information on _what_ to do to a single dataset, but not on how to reason or
talk about multiple deidentifying processess, their differences, their characteristics.

## For whom?
People developing or maintaining image deidentification pipelines.

## What is it?
An information model first and foremost. Concept definitions with clear descriptions of
their relations. There might be python code to define constants, transformations between objects maybe.

## What is it not?
Anything that does any actual image processing. No loading of DICOM files anywhere.

## For docs editors
### Render html docs
Go to 
(in docs/build): `make docs_html`

### Fancy auto-updating 
Auto-reload a html view as you change the docs source.
Requirements:
* Linux or WSL (this uses some subshell and piping tricks)
* [entr](https://github.com/eradman/entr) - Run a command when files change. Apt install this
* [livereload](https://livereload.readthedocs.io/en/latest/index.html) - Serve local files and auto-reload on change. Python lib found as dev dependency in midom.
* Possibly firefox to make livereload work properly

Steps:
* Start a shell in this midom base dir (where Makefile is) 
* run `uv run make launch_source_listener`
* Open the livereload url printed in the script output. By default this is http://127.0.0.1:35729/

You might have to reload the page once to link livereload to the browser. After that, any
save to a `.rst` or `.puml` file will trigger rebuild of docs/build, which will in turn
trigger a page reload