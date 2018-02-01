
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

from data import colours

from os.path import join, dirname, abspath
import time

class NeuralNetAI(AI):
    name = ''

    def __init__(self, *args, stepsize=0.05, restore=False, prob_factor=1., **kwargs):
        super(NeuralNetAI, self).__init__(*args, **kwargs)
        self.stepsize = stepsize
        self.prob_factor = prob_factor
        self.make_graph()


        if restore:
            self.load_variables()

    def make_graph(self):
        raise NotImplementedError()

    def ckpt_filen(self):
        return join(dirname(abspath(__file__)), 'saves', '{}.ckpt'.format(self.name))

    def load_variables(self):
        print('filen', self.ckpt_filen())
        print('RESTORING')
        self.saver.restore(self.session, self.ckpt_filen())

    def make_move(self, state):
        # t1 = time.time()
        moves = state.get_valid_moves(state.current_player_index)

        if len(moves) == 0:
            print('passing')
            return (('gems', {}))
        # t2 = time.time()
        # print('getting moves time', t2 - t1)
        # print()
        # print('moves are', '\n'.join(map(str, moves)))

        current_player_index = state.current_player_index
        new_states = [state.copy().make_move(move) for move in moves]
        vectors = np.array([new_state.get_state_vector(current_player_index) for new_state in new_states])

        # outputs = self.session.run(self.output, {self.input_state: vectors}).reshape([-1])
        # import ipdb
        # ipdb.set_trace()
        # exit(1)

        # probabilities = self.session.run(tf.nn.softmax(outputs * 10))
        try:
            probabilities = self.session.run(self.probabilities, {self.input_state: vectors})
        except ValueError:
            print('Error calculating self.probabilities - maybe there are no available moves')
            import ipdb
            ipdb.set_trace()
        # print('probabilities', probabilities)

        probabilities = probabilities

        player_probabilities = probabilities[state.current_player_index]

        # probabilities /= np.sum(probabilities)
        # print('probabilities are', probabilities)
        index = np.random.choice(range(len(moves)), p=player_probabilities)
        # print('index is', index, np.argmax(probabilities))
        choice = moves[index]
        # choice = moves[np.argmax(probabilities)]
        # print('choice is', choice)
        
        # if len(probabilities) < 30:
        #     import ipdb
        #     ipdb.set_trace()

        return choice

class H50AI(NeuralNetAI):
    name = '2ph50'

    def make_graph(self):
        INPUT_SIZE = 585 # 613 # 294 # 613
        # INPUT_SIZE = 293 # 294 # 613
        HIDDEN_LAYER_SIZE = 20

        input_state = tf.placeholder(tf.float32, [None, INPUT_SIZE])
        weight_1 = tf.Variable(tf.truncated_normal([INPUT_SIZE, HIDDEN_LAYER_SIZE], stddev=0.5))
        bias_1 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE], stddev=0.5))

        # output = tf.matmul(input_state, weight_1) + bias_1

        hidden_output_1 = tf.nn.tanh(tf.matmul(input_state, weight_1) + bias_1)

        weight_2 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE, 2], stddev=0.5))
        bias_2 = tf.Variable(tf.truncated_normal([2], stddev=0.5))

        stepsize_variable = tf.placeholder(tf.float32, shape=[])
        stepsize_multiplier = tf.placeholder(tf.float32, shape=[])

        # output = tf.nn.sigmoid(tf.matmul(hidden_output_1, weight_2) + bias_2)
        output = tf.matmul(hidden_output_1, weight_2) + bias_2

        real_result = tf.placeholder(tf.float32, [None, 2])

        # train_step = tf.train.GradientDescentOptimizer(stepsize_variable * stepsize_multiplier).minimize((real_result - output)**2)
        train_step = tf.train.GradientDescentOptimizer(stepsize_variable * stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output)))

        session = tf.Session()
        tf.global_variables_initializer().run(session=session)

        accuracy = tf.reduce_mean((real_result - output)**2)

        self.input_state = input_state
        self.output = output
        self.real_result = real_result
        self.session = session
        self.train_step = train_step
        self.accuracy = accuracy

        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.bias_1 = bias_1
        self.bias_2 = bias_2
        self.hidden_output_1 = hidden_output_1

        self.stepsize_variable = stepsize_variable
        self.stepsize_multiplier = stepsize_multiplier

        self.saver = tf.train.Saver()

        # self.probabilities = tf.nn.softmax(tf.reshape(output, [-1]) * 1)
        # self.probabilities = tf.nn.softmax(tf.reshape(output, [2, -1]))
        self.probabilities = tf.nn.softmax(tf.transpose(output) * self.prob_factor)
        
    def print_info(self):
        print('weight 1:\n', self.weight_1.eval(self.session))
        print('bias 1:\n', self.bias_1.eval(self.session))
        print('weight 2:\n', self.weight_2.eval(self.session))
        # print('bias 2:\n', self.bias_2.eval(self.session))
