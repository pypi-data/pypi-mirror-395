# Ephemeral Buffer API

## Overview
This project represent the reference implementation of **Ephemeral buffer** concept.
A full description of the concept is available in *[the ephemeral buffer proposal](docs/2025.12.03-EphemeralBuffers-v2.md)*

## Installation

The installation is the standard installation procedure of any WSGI python library. See details below.

### From source code

Clone the repository [ebuffer](https://gitlab.aqmo.org/numpex/ebuffer.git):

```sh
git clone https://public:uhpzy8bFXwcYszCtkkcU@gitlab.aqmo.org/numpex/ebuffer.git
# Navigate into the project directory
cd ebuffer

# Create and load a virtual environment
python3 -mvenv venv
source venv/bin/activate
```

#### Local Deployment
For a local deployment install the server dependencies :
```sh
# Install dependencies for local deployment
pip install -r requirements-server.txt
```

#### For an WSGI Server
The core dependencies are in *requirements.txt*:
```sh
# Install core dependencies for an WSGI web server
pip install -r requirements.txt
```

## Authentication

The authentication mechanism depends on backends, and each depends on
a particular configuration.  All actions that a user can operate on a
ephemeral buffer required a **Bearer Token**. This token is received
after the authentication process from keycloak (IDP used). The token
has a limited lifetime and can be refresh.

## Usage
To Run the project, start the server : `fastapi dev server/src/main.py`

A swagger documentation is available on  `http://127.0.0.1:8000/docs/ui`

