import json
import re
from typing import List, Dict
import os

SPECIAL_TOKENS = {
    "<BOS>": 256,
    "<EOS>": 257,
    "<UNK>": 258,
}

class Tokenizer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        vocab_path = os.path.join(current_dir, 'vocab.json')
        if not os.path.exists(vocab_path):
            raise FileNotFoundError(f"Could not find vocab file at: {vocab_path}")
        
        with open(vocab_path, 'r', encoding='utf-8') as f:
            self.__merges = json.load(f)
            
        self.__vocab = {i: bytes([i]) for i in range(256)}
        self.__special_tokens = SPECIAL_TOKENS.copy()
        for key, idx in self.__merges.items():
            p0, p1 = map(int, key.split(','))
            self.__vocab[idx] = self.__vocab[p0] + self.__vocab[p1]
        
        for token_str, _id in self.__special_tokens.items():
            self.__vocab[_id] = token_str.encode("utf-8")
        
        self.__get_id_to_token = {idx: token.decode('utf-8', errors='replace') if isinstance(token, bytes) else token for idx, token in self.__vocab.items()}
        self.__get_token_to_id = {v: k for k, v in self.__get_id_to_token.items()}

    def __compute_pair_stats(self, ids):
        counts = {}
        for pair in zip(ids, ids[1:]):
            counts[pair] = counts.get(pair, 0) + 1
        return counts

    def __merge_ids(self, ids, pair, idx):
        newids=[]
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids
    
    def token_to_id(self, token : str) -> int:
        return self.__get_token_to_id.get(token, self.__special_tokens["<UNK>"])
    
    def id_to_token(self, idx : int) -> str:
        return self.__get_id_to_token.get(idx, "<UNK>")
    
    def encode(self, text : str, add_special_tokens : bool=False) -> List[int]:
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            stats = self.__compute_pair_stats(ids)
            pair_key = lambda p: f"{p[0]},{p[1]}"
            pair = min(stats, key=lambda p: self.__merges.get(pair_key(p), float("inf")))
            if pair_key(pair) not in self.__merges:
                break
            idx = self.__merges[pair_key(pair)]
            ids = self.__merge_ids(ids, pair, idx)
        
        if add_special_tokens: 
            return [self.__special_tokens["<BOS>"]] + ids + [self.__special_tokens["<EOS>"]]
        return ids
    
    def encode_batch(self, texts : List[str], add_special_tokens : bool=False) -> List[List[int]]:
        return [self.encode(text, add_special_tokens) for text in texts]
    
    def decode(self, ids : List[int], skip_special_tokens : bool=True) -> str:
        if skip_special_tokens:
            special_ids = set(self.__special_tokens.values())
            ids = [i for i in ids if i not in special_ids]
            
        tokens = b"".join(self.__vocab[idx] for idx in ids)
        return tokens.decode("utf-8", errors="replace")
    
    def vocab_size(self) -> int:
        return len(self.__vocab)
    
    def token_count(self, text : str) -> int:
        return len(self.encode(text))
    
    def tokenize(self, text : str) -> List[str]:
        return re.findall(r'\w+|[^\w\s]', text)
    
    def normalize_text(self, text : str, lower: bool=True, remove_punct : bool=False) -> str:
        if lower:
            text = text.lower()
        if remove_punct:
            text = re.sub(r'[^\w\s]', '', text)
            
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def debug(self, text : str) -> List[Dict]:
        encoded = self.encode(text)
        ans = []
        for i in encoded:
            ans.append({"token" : self.decode([i]), "id" : i})
        return ans