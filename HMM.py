import cProfile
import random
import numpy as np
import torch
from pomegranate.distributions import Categorical
from pomegranate.hmm import SparseHMM

def max_index(tensor) -> []:
    result = []
    for row in tensor:
        max_value, max_index = torch.max(row, dim=0)
        result.append(max_index.item())
    return result

class HMM:
    def __init__(self):
        self.db=''
        self.model=None

    def HiddenMarkovModels(self,pre: str,fit: bool):
        if len(self.db)<11:
            self.db=self.db+pre
            return 'Too few datasets'

        S = Categorical([[0.9, 0.05, 0.05]])
        JB = Categorical([[0.15, 0.425, 0.425]])
        J = Categorical([[0.05, 0.9, 0.05]])
        SB = Categorical([[0.425, 0.15, 0.425]])
        B = Categorical([[0.05, 0.05, 0.9]])
        JS = Categorical([[0.425, 0.425, 0.15]])
        R = Categorical([[0.33, 0.33, 0.34]])

        edges = [
            [R, R, 0.39],
            [R, B, 0.1], [R, JS, 0.1],
            [R, J, 0.1], [R, SB, 0.1],
            [R, S, 0.1], [R, JB, 0.1],
            [B, B, 0.39],
            [B, S, 0.1], [B, JS, 0.1],
            [B, J, 0.1], [B, SB, 0.1],
            [B, R, 0.1], [B, JB, 0.1],
            [S, S, 0.39],
            [S, B, 0.1], [S, JS, 0.1],
            [S, J, 0.1], [S, SB, 0.1],
            [S, R, 0.1], [S, JB, 0.1],
            [J, J, 0.39],
            [J, S, 0.1], [J, JS, 0.1],
            [J, R, 0.1], [J, SB, 0.1],
            [J, B, 0.1], [J, JB, 0.1],
            [JS, JS, 0.39],
            [JS, SB, 0.1], [JS, B, 0.1],
            [JS, JB, 0.1], [JS, S, 0.1],
            [JS, R, 0.1], [JS, J, 0.1],
            [JB, JB, 0.39],
            [JB, SB, 0.1], [JB, B, 0.1],
            [JB, JS, 0.1], [JB, S, 0.1],
            [JB, R, 0.1], [JB, J, 0.1],
            [SB, SB, 0.39],
            [SB, JB, 0.1], [SB, B, 0.1],
            [SB, JS, 0.1], [SB, S, 0.1],
            [SB, R, 0.1], [SB, J, 0.1]
        ]
        self.db += pre
        self.db = [char for char in self.db if char in ['S', 'J', 'B']]  # 过滤掉不在['S', 'J', 'B']中的字符
        X = np.array([[[['S', 'J', 'B'].index(char)] for char in self.db[-10:]]])
        if self.model is None:
            self.model = SparseHMM([R, B, J, S, SB, JB, JS], edges=edges, starts=[0.94, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],ends=[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        if fit is True:
            Y = np.array([[[['S', 'J', 'B'].index(char)] for char in self.db]])
            self.model.fit(Y)
        proba = self.model.predict_proba(X)[0]
        predict = max_index(proba)
        dic = {1: 'its: cloth', 2: 'its: scissors', 3: 'its: stone'}
        for i in predict:
            if i == 0:
                return random.choice([dic[1], dic[2], dic[3]])
            elif i == 1 or i == 2 or i == 3:
                return dic[i]
            elif i == 4:
                if pre[-1] == 'S': return dic[1]
                if pre[-1] == 'B': return dic[2]
            elif i == 5:
                if pre[-1] == 'J': return dic[3]
                if pre[-1] == 'B': return dic[2]
            else:
                if pre[-1] == 'J': return dic[3]
                if pre[-1] == 'S': return dic[2]

