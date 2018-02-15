
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
            return (('gems', {}), [0.5, 0.5])
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

        probability = self.session.run(self.softmax_output, {self.input_state: vectors[index].reshape(1, -1)})[0]

        return choice, probability

    def train(self, training_data, stepsize_multiplier=1., stepsize=0.01):
        for winner_index, state_vectors in training_data:
            vs = [v[0] for v in state_vectors]
            expected_output = np.zeros(2)
            expected_output[winner_index] = 1 
            for _ in range(10):
                try:
                    self.session.run(self.train_step, feed_dict={
                        self.input_state: np.array(vs),
                        self.real_result: np.array([expected_output for _ in vs]),
                        self.stepsize_multiplier: stepsize_multiplier, 
                        self.stepsize_variable: stepsize,
                        })
                except ValueError:
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()

class H50AI(NeuralNetAI):
    name = '2ph50'

    def make_graph(self):
        INPUT_SIZE = 265 # 305 # 265 # 585 
        # INPUT_SIZE = 293 # 294 # 613
        HIDDEN_LAYER_SIZE = 20

        input_state = tf.placeholder(tf.float32, [None, INPUT_SIZE])
        weight_1 = tf.Variable(tf.truncated_normal([INPUT_SIZE, HIDDEN_LAYER_SIZE], stddev=0.5),
                               name='weight_1')
        bias_1 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE], stddev=0.5),
                             name='bias_1')

        # output = tf.matmul(input_state, weight_1) + bias_1

        hidden_output_1 = tf.nn.tanh(tf.matmul(input_state, weight_1) + bias_1)

        weight_2 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE, 2], stddev=0.5),
                               name='weight_2')
        bias_2 = tf.Variable(tf.truncated_normal([2], stddev=0.5),
                             name='bias_2')

        stepsize_variable = tf.placeholder(tf.float32, shape=[])
        stepsize_multiplier = tf.placeholder(tf.float32, shape=[])

        # output = tf.nn.sigmoid(tf.matmul(hidden_output_1, weight_2) + bias_2)
        output = tf.matmul(hidden_output_1, weight_2) + bias_2
        softmax_output = tf.nn.softmax(output)

        real_result = tf.placeholder(tf.float32, [None, 2])

        # train_step = tf.train.GradientDescentOptimizer(stepsize_variable * stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output)))
        train_step = tf.train.AdamOptimizer(stepsize_variable * stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output)))

        session = tf.Session()
        tf.global_variables_initializer().run(session=session)

        accuracy = tf.reduce_mean((real_result - output)**2)

        self.input_state = input_state
        self.output = output
        self.softmax_output = softmax_output
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
        self.probabilities = tf.nn.softmax(tf.transpose(softmax_output) * self.prob_factor)

        self.trainable_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
                                                     scope=tf.get_variable_scope().name)
        
    def print_info(self):
        print('weight 1:\n', self.weight_1.eval(self.session))
        print('bias 1:\n', self.bias_1.eval(self.session))
        print('weight 2:\n', self.weight_2.eval(self.session))
        # print('bias 2:\n', self.bias_2.eval(self.session))


class H50AI_TD(H50AI):
    name = '2ph50_td'

    def __init__(self, **kwargs):
        with tf.variable_scope(self.name):

            super(H50AI_TD, self).__init__(**kwargs)

            self.opt = tf.train.AdamOptimizer()
            self.grads = tf.gradients(self.softmax_output[:, 0], self.trainable_variables)
            self.grads_s = [tf.placeholder(tf.float32, shape=tvar.get_shape(), name='{}{}{}'.format(i,i,i))
                            for i, tvar in enumerate(self.trainable_variables)]
            self.apply_grads = self.opt.apply_gradients(zip(self.grads_s, self.trainable_variables),
                                                        name='apply_grads')

    def make_move(self, state):
        index = state.current_player_index
        grads = self.session.run(self.grads, feed_dict={
            self.input_state: state.get_state_vector(index).reshape(1, -1)})
        move, probability = super(H50AI_TD, self).make_move(state)
        vec = state.get_state_vector(index)
        # import ipdb
        # ipdb.set_trace()
        # print(move, probability, sum([a * b**2 for a, b in zip(v, range(len(v)))]))
        return move, probability, grads

    def train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        # lambda_param = 0.7

        # traces = [np.zeros(tvar.shape) for tvar in self.trainable_variables]

        print('ai.train')
        # import ipdb
        # ipdb.set_trace()

        for row_index, row in enumerate(training_data):
            print('Training game {} / {}'.format(row_index, len(training_data)))
            winner_index, state_vectors = row
            print(state_vectors[-1][1], winner_index)
            previous_move, previous_value, previous_grads = state_vectors[0]
            for move, value, grads in state_vectors[1:]:
                try:
                    delta = value[0] - previous_value[0]
                    delta *= -1**(winner_index)
                    feed_dict = {grad_var: -delta * previous_grad# * stepsize
                                for previous_grad, grad_var in zip(previous_grads, self.grads_s)}
                    # import ipdb
                    # ipdb.set_trace()
                    print([np.sum(g) for g in previous_grads])
                    self.session.run(self.apply_grads,
                                    feed_dict=feed_dict)
                except (ValueError, IndexError):
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()
                    print('...')

                previous_move = move
                previous_value = value
                previous_grads = grads
                
