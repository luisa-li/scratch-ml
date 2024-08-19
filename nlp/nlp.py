"""General NLP classes and methods, referenced primarily from d2l."""

import collections 

class Vocab:
    
    def __init__(self, tokens=[], min_freq=0, reserved_tokens=[]):
        
        # get all tokens
        if tokens and isinstance(tokens[0], list):
            tokens = [token for line in tokens for token in line]
        
        # token frequencies
        counter = collections.Counter(tokens)
        self.token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        
        # get list of unique tokens, and the dictionaries to translate between id and token
        filtered = [token for token, freq in self.token_freqs if freq >= min_freq]
        self.idx_to_token = list(sorted(set(['<unk>'] + reserved_tokens + filtered)))
        self.token_to_idx = {token: idx for idx, token in enumerate(self.idx_to_token)}
        
    def __len__(self):
        return len(self.idx_to_token)
    
    def __getitem__(self, tokens):
        if not isinstance(tokens, (list, tuple)):
            # returns the token and if it doesn't exist, return the <unk>
            return self.token_to_idx.get(tokens, self.unk) 
        return [self.__getitem__(token) for token in tokens]
    
    def to_tokens(self, indices):
        # convert one by one 
        if hasattr(indices, '__len__') and len(indices) > 1:
            return [self.idx_to_token[int(index)] for index in indices]
        # or just convert the one
        return self.idx_to_token[indices]
    
    @property
    def unk(self):
        return self.token_to_idx['<unk>']
        
    