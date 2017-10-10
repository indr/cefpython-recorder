# CEF Python Recorder

This repository contains scripts to play and/or record videos from websites using [CEF Python](https://github.com/cztomczak/cefpython). The Python script `capture.py` is a modification based on the `screenshot.py` script from the CEF Python examples.


## Installation

In order to use the scripts provided in this repository, install `cefpython` using pip tool:

```bash
pip install cefpython3==57.0
```


## Usage

Use `capture.py` to capture frames and write them to an output file. The script expects five arguments: url, width, height, fps, outfile:

```bash
python capture.py https://github.com/indr/cef-python 1024 768 25 output.bgra
```

## Examples

This repository contains scripts and web pages to demonstrate playing and recording. In order to run the examples, you need to start a simple web server by running `serve.sh`. Capture the website with `capture.sh` and then either play it with `play.sh` or record to a file using `record.sh`.


## Copyright and License

Copyright (c) 2017 Reto Inderbitzin, [MIT](LICENSE) License
