# papaWhaled

---

## Description

**papaWhaled** is Flask API server that helps deploy CTF challenges. It automatically generates dockerfile, builds image, and runs container. Also, with the help of nsjail@google, it can isolate most of challenges. 

---

## Installation

    git clone https://github.com/Hhro/papaWhaled \
    pip install virtualenv \
    virtualenv -p python3 papaWhaled_env \
    source ./papaWhaled_env/bin/activate \
    pip install -r requirements.txt \

---

## Requirements

It requires following python3 modules. 

    virtualenv
    pathlib
    flask
    flask_restful
    flask_cors
    docker
    pytest

You can install these modules by `pip isntall -r requirements.txt`

It also requires following docker image.

    nsjail

You can find **nsjail** at [https://github.com/google/nsjail](https://github.com/google/nsjail). 

⚠Currently, nsjail is based on *ubuntu16.04.* If you need to deploy challenge on other environment you must build nsjail yourself. Find help at [here](https://www.notion.so/Build-custom-nsjail-image-be96f6c70a8c4212b80992f650d4ddc0).

---

## Usage

    usage: app.py [-h] --supplier SUPPLIER [--ssl] [--pem PEM] [--crt CRT] [-d]
                  [-p PORT] [--backup] [--prefix PREFIX]
    
    optional arguments:
      -h, --help            show this help message and exit
      --supplier SUPPLIER   Supplier path
      --ssl                 Run server on SSL.
      --pem PEM             SSL pem key. Required if you run on ssl mode.
      --crt CRT             SSL certificate. Required if you run on ssl mode.
      -d, --debug           Run flask server as debug mode
      -p PORT, --port PORT  API server port. Default is 31337
      --backup              On error, back up the challenge directory as name.bak
      --prefix PREFIX       Prefix of name of live challenge container.

---

## Features

It provides following features.

- **List**
Simply listing challenges deployed on challenge server.
- **Deploy**

    Currently, two types of deploying is available. 

    1. **docker**
    Challenge would be run in jailed docker container.
    2. **non_docker : not-implemented**
- **Restart**
Rerun the challenge.
- **Terminate**
Stop challenge, and delete every resources about challenge.

---

## ⚠Security notes

NEVER EVER expose API server. There is no guarantee of security. There are even vulnerabilities that have already been discovered but have not been fixed. So be careful to use it until I fix it.

---

## To-Do

1. Security patch: [Censored]
2. non-docker

---

## Docs

[APIs(v1.1)](docs/APIs_v1_1.md)

[Build custom nsjail image](docs/Build_custom_nsjail_image.md)

[How to write test script?](docs/How_to_write_test_script.md)

[Deploy options](docs/Deploy_options.md)

[Library cache](docs/Library_cache.md)