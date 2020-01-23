#!/bin/bash
source ./papaWhaled_env/bin/activate
nohup python app.py -d -p 31337 --supplier /home/hhro/papaWhaled/supplier/ --pem ssl/hhro.key --crt ssl/hhro.crt --ssl &
