import spacy
import re
import os

class BlockLenAdjuster:
    def __init__(self, input_dir, min_block_len=50, max_block_len=100):
        self.input_dir = input_dir
       
        self.nlp = spacy.load("en_core_web_sm")
        self.min_block_len = min_block_len
        self.max_block_len = max_block_len
        
    def compact_paragraph(self, file_name):
        
        with open(os.path.join(self.input_dir, file_name), 'r') as f: 
            raw_content = f.read()
        compacted_content = re.sub(r'\n+', '\n', raw_content).strip()
        with open(os.path.join(self.input_dir, f'proc_{file_name}'), 'w') as f: 
            f.write(compacted_content)
            
    def merge(self, file_name):
        with open(os.path.join(self.input_dir, file_name), 'r') as f: 
            raw_content = f.read()
        merged_content = re.sub(r'\n+', ' ', raw_content).strip()
        with open(os.path.join(self.input_dir, f'proc_{file_name}'), 'w') as f: 
            f.write(merged_content)
        
    def adjust(self, file_name):
        
        with open(os.path.join(self.input_dir, file_name), 'r') as f: 
            raw_content = f.read()
        raw_content = re.sub(r'\n+', '\n', raw_content).strip()
        raw_content_blocks = raw_content.split('\n')
        adjusted_content_blocks = []
        
        staging = []
        staging_token_count = 0
        
        for block in raw_content_blocks:
            block_doc = self.nlp(block)
            if len(block_doc) + staging_token_count > self.min_block_len:
                if len(block_doc) + staging_token_count < self.max_block_len:
                    staging.append(block)
                    to_add = ' '.join(staging)
                    adjusted_content_blocks.append(to_add)
                    staging = []
                    staging_token_count = 0
                else:
                    to_add = ' '.join(staging)
                    adjusted_content_blocks.append(to_add)
                    staging = [block]
                    staging_token_count = len(block_doc)     
            else:
                staging.append(block)
                staging_token_count += len(block_doc)
        
        if len(staging) > 0:
            to_add = ' '.join(staging)

            adjusted_content_blocks.append(to_add)

        proc_content = "\n".join(adjusted_content_blocks)
        proc_content = re.sub(r'\n+', '\n', proc_content).strip()
        proc_content = proc_content.strip("\n")
        
        with open(os.path.join(self.input_dir, f'proc_{file_name}'), 'w') as f: 
            f.write(proc_content)
            
            
class Config:
    def __init__(self):
        self.task = 'abs'
        self.encoder = 'bert'
        self.mode = 'test_text'
        self.bert_data_path = '../bert_data_new/cnndm'
        self.model_path = '../models/'
        self.result_path = ''
        self.temp_dir = '../temp'
        self.text_src = ''
        self.text_tgt = ''
        
        self.batch_size = 140
        self.test_batch_size = 200
        self.max_ndocs_in_batch = 6
        
        self.max_pos = 512
        self.use_interval = True
        self.large = False
        self.load_from_extractive = ''
        
        self.sep_optim = False
        self.lr_bert = 2e-3
        self.lr_dec = 2e-3
        self.use_bert_emb = False
        
        self.share_emb = False
        self.finetune_bert = True
        self.dec_dropout = 0.2
        self.dec_layers = 6
        self.dec_hidden_size = 768
        self.dec_heads = 8
        self.dec_ff_size = 2048
        self.enc_hidden_size = 512
        self.enc_ff_size = 512
        self.enc_dropout = 0.2
        self.enc_layers = 6
        
        self.ext_dropout = 0.2
        self.ext_layers = 2
        self.ext_hidden_size =768
        self.ext_heads = 8 
        self.ext_ff_size = 2048
        
        self.label_smoothing = 0.1
        self.generator_shard_size = 32
        self.alpha = 0.6
        self.beam_size = 5
        self.min_length = 15
        self.max_length = 150
        self.max_tgt_len = 140
        
        self.param_init = 0
        self.param_init_glorot = True
        self.optim =  'adam'
        self.lr = 1 
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.warmup_steps = 8000
        self.warmup_steps_bert = 8000
        self.warmup_steps_dec = 8000
        self.max_grad_norm = 0
        
        self.save_checkpoint_steps = 5
        self.accum_count = 1
        self.report_every = 1
        self.train_steps = 1000
        self.recall_eval = False
        
        self.visible_gpus = '0'
        self.gpu_ranks = '0'
        self.log_file = './logs/pred.log'
        self.seed = 666
        
        self.test_all = False
        self.test_from = ''
        self.test_start_from = -1
        
        self.train_from = ''
        self.report_rouge = True
        self.block_trigram = True
        
        self.input_path = '../input_raw_text/'
        self.output_path = '../pred/'
        
        
            
            
                
        