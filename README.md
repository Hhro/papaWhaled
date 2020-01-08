# papaWhaled

## Description

**papaWhaled** is Flask API server that helps deploy CTF challenges. It automatically generates dockerfile, builds image, and runs container. Also, with the help of nsjail@google, it can isolate most of challenges. 



---

## Installation

    git clone https://github.com/Hhro/papaWhaled \
    pip install virtualenv \
    virtualenv -p python3 papaWhaled_env \
    source ./papaWhaled_env/bin/activate \
    pip install -r requirements.txt \
    python app.py --SUPPLIER=./supplier/



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

⚠Currently, nsjail is based on *ubuntu16.04.* If you need to deploy challenge on other environment you must build nsjail yourself. Find help at [here](docs/build_custom_nsjail_image.md).



---

## Features

It provides following features.

- **List**
  Simply listing challenges deployed on challenge server.

- **Deploy**

    Currently, two types of deploying is available. 

    1. **auto**
    Three docker process(Generate, build and run) is fully handled by papaWhaled. It is only available in certain circumstance.
    2. **custom docker**
    If challenge has several dependency, you may need to use this mode. In this deploying mode, you can make dockerfile yourself. **papaWhaled** only build your dockerfile and run.

    Fully customizable mode would be added.

- **Restart**
  Rerun the challenge.

- **Terminate**
  Remove challenge container, and delete every resources about challenge.

  

---

## Docs

[APIs](docs/APIs.md)

[Build custom nsjail image](docs/build_custom_nsjail_image.md)

[How to write test script?](docs/how_to_write_test_script.md)

