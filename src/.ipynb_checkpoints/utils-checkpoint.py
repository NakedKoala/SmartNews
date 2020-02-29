import spacy
import re
import os

class BlockLenAdjuster:
    def __init__(self, input_dir, min_block_len=300, max_block_len=500):
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
        
        with open(os.path.join(self.input_dir, f'proc_{file_name}'), 'w') as f: 
            f.write(proc_content)
            
                
        