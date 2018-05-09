
from nn import H50AI_TDlam

import json

ai = H50AI_TDlam(restore=True)

weight_1, bias_1, weight_2, bias_2 = ai.session.run(
    [ai.weight_1, ai.bias_1, ai.weight_2, ai.bias_2])

js_str = json.dumps({'weight_1': weight_1.tolist(),
                     'weight_2': weight_2.tolist(),
                     'bias_1': bias_1.tolist(),
                     'bias_2': bias_2.tolist()})

with open('weights.js', 'w') as fileh:
    fileh.write('weights = {}'.format(js_str))
