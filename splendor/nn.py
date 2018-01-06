
inputs = '''
each card in pile = 90
each card available to buy = 90
each card in opponent's hand = 90
each card in own hand = 90
each gem colour num available = 50
each gem colour num held by opponent = 50 * o
each gem colour num held by self = 50
each card colour num held by self = 50
each card colour num held by opponent = 50 * o
current points = 1
opponent points = o
'''

from aibase import AI

import tensorflow as tf
import numpy as np

from os.path import join, dirname, abspath

class NeuralNetAI(AI):
    name = ''

    def __init__(self, *args, stepsize=0.005, restore=False, **kwargs):
        super(NeuralNetAI, self).__init__(*args, **kwargs)
        self.stepsize = stepsize
        self.make_graph()

        if restore:
            self.load_variables()

    def make_graph(self):
        raise NotImplementedError()

    def ckpt_filen(self):
        return join(dirname(abspath(__file__)), 'saves', '{}.ckpt'.format(self.name))

    def load_variables(self):
        print('filen', self.ckpt_filen())
        self.saver.restore(self.session, self.ckpt_filen())

    def make_move(self, state):
        moves = state.get_valid_moves(state.current_player_index)
        # print()
        # print('moves are', '\n'.join(map(str, moves)))

        new_states = [state.copy().make_move(move) for move in moves]
        vectors = np.array([new_state.get_state_vector() for new_state in new_states])

        outputs = self.session.run(self.output, {self.input_state: vectors}).reshape([-1])

        probabilities = self.session.run(tf.nn.softmax(outputs))

        choice = moves[np.random.choice(range(len(moves)), p=probabilities)]
        

        return choice

class H50AI(NeuralNetAI):
    name = '2ph50'

    def make_graph(self):

        input_state = tf.placeholder(tf.float32, [None, 613])
        weight_1 = tf.Variable(tf.truncated_normal([613, 50], stddev=0.05))
        bias_1 = tf.Variable(tf.truncated_normal([50], stddev=0.05))

        hidden_output_1 = tf.nn.relu(tf.matmul(input_state, weight_1) + bias_1)

        weight_2 = tf.Variable(tf.truncated_normal([50, 1], stddev=0.05))
        bias_2 = tf.Variable(tf.truncated_normal([1], stddev=0.05))

        output = tf.nn.relu(tf.matmul(hidden_output_1, weight_2) + bias_2)

        real_result = tf.placeholder(tf.float32, [None, 1])

        train_step = tf.train.GradientDescentOptimizer(self.stepsize).minimize((real_result - output)**2)

        session = tf.Session()
        tf.global_variables_initializer().run(session=session)

        accuracy = tf.reduce_mean((real_result - output)**2)

        self.input_state = input_state
        self.output = output
        self.real_result = real_result
        self.session = session
        self.train_step = train_step
        self.accuracy = accuracy

        self.saver = tf.train.Saver()
        
