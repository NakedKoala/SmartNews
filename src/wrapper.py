from utils import BlockLenAdjuster, Config
import torch
from pytorch_transformers import BertTokenizer
from models.model_builder import AbsSummarizer
from models.predictor import build_predictor
from others.logging import logger, init_logger
from models.data_loader import load_text
import os
import spacy


class SmartNews:
    def __init__(self, config):
        self.config = config 
        self.adjuster = BlockLenAdjuster(input_dir=config.input_path)
        logger.info('Loading checkpoint from %s' % config.test_from)
        self.device = "cpu" if config.visible_gpus == '-1' else "cuda"
    
        checkpoint = torch.load(config.test_from, map_location=lambda storage, loc: storage)
        opt = vars(checkpoint['opt'])
        
        model_flags = ['hidden_size', 'ff_size', 'heads', 'emb_size', 'enc_layers', 'enc_hidden_size', 'enc_ff_size',
               'dec_layers', 'dec_hidden_size', 'dec_ff_size', 'encoder', 'ff_actv', 'use_interval']
        for k in opt.keys():
            if (k in model_flags):
                setattr(config, k, opt[k])
        print(config)

        model = AbsSummarizer(self.config, self.device, checkpoint)
        model.eval()
   
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True, cache_dir=config.temp_dir)
        symbols = {'BOS': tokenizer.vocab['[unused0]'], 'EOS': tokenizer.vocab['[unused1]'],
                   'PAD': tokenizer.vocab['[PAD]'], 'EOQ': tokenizer.vocab['[unused2]']}
        self.predictor = build_predictor(config, tokenizer, symbols, model, logger)
        self.nlp = spacy.load('en_core_web_sm')
        
    def summarize(self, file_name):
        self.adjuster.compact_paragraph(file_name)
        self.config.text_src =  os.path.join(self.config.input_path, f'proc_{file_name}') 
        self.config.result_path = os.path.join(self.config.output_path, f'result_{file_name}')
        test_iter = load_text(self.config,  self.config.text_src, '', self.device)
        self.predictor.translate(test_iter, -1)
        return self.diagnostic(self.config)
        
    def diagnostic(self, config):
        
        with open(config.text_src, 'r') as f:
            in_file_content = f.read()
            doc_input = self.nlp(in_file_content)
        with open(config.result_path,'r') as f:
            out_file_content = f.read()
            doc_output = self.nlp(out_file_content)
            
        input_token = len(doc_input)
        output_token = len(doc_output)
        compress_ratio = output_token / input_token 
        return {
            'input_token': input_token,
            'output_token': output_token,
            'compress_ratio': compress_ratio
        }
        
        