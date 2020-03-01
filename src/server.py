from flask import Flask, request, jsonify, send_file
from utils import Config 
from wrapper import SmartNews
import json

def init_model():
    config = Config()
    config.test_from = '../models/model_step_148000.pt'
    model = SmartNews(config)
    return model

app = Flask(__name__)
model = init_model()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/summarize', methods=['POST'])
def summarize():
#     import pdb 
#     pdb.set_trace()
    file_handle = request.files['upfile']
    file_name=  file_handle.filename
    file_handle.save(f'../input_raw_text/{file_name}')
    analytics = model.summarize(file_name)
    
    with open(f'../pred/result_{file_name}','r') as f:
        summarized_text = f.read()
    
    res = {
      'analytics': analytics,
      'summarized_text': summarized_text
    }
        
    return jsonify(res)

