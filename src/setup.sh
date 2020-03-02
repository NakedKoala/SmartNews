#!/bin/bash

pip install -U spacy 
python -m spacy download en_core_web_sm
pip install -r ../requirements.txt
pip install flask
export FLASK_APP=/home/ec2-user/SmartNews/src/server.py
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-IKVCtc4Q-BdZpjXc4s70_fRsWnjtYLr' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-IKVCtc4Q-BdZpjXc4s70_fRsWnjtYLr" -O bertsumextabs_cnndm_final_model.zip && rm -rf /tmp/cookies.txt

unzip bertsumextabs_cnndm_final_model.zip -d ../models/


