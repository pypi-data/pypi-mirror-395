# opengamedata-api-utils

Repository for utility server-side script and classes used by OpenGameData APIs.

## Contents

### Python Package

The `utils` repository contains a package that can be installed from `pip`, and places its classes under the `ogd.apis` namespace.
The available modules include:

* `HelloAPI.py` : Class for creating a "Hello, World" API to aid in testing deploys of other APIs.
* `schemas` : Contains a base class for server config schemas to handle version and debug-level config items
* `utils` : Contains helper classes for API requests and responses, as well as general-purpose parsing and setup functions.

### Data Store Utilities

The `store` directory contains a script for reindexing a folder of OGD datasets after new datasets have been added.
This index is used by the FileAPI to check what datasets are available on the server.

## Getting Started

### Hello World of Flask

Steps to run:

1. Check out latest `opengamedata-server`.
2. Run `pip install -r requirements.txt` to ensure you've got flask.
3. Run `flask run`.
4. Open localhost:5000 or localhost:5000/hello to see some really basic text output from the Flask server.

If Flask doesn't run, it's possible you'd need to first export FLASK_APP as an environment variable, set to "wsgi" (so in Bash, export FLASK_APP=wsgi).
However, the script is named wsgi.py specifically because Flask is supposed to auto-detect it. So if this issue ever did come up, please ping Luke so he can look into it.
