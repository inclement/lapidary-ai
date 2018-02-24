
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

from aibase import AI, MoveInfo

import tensorflow as tf
import numpy as np

from data import colours

from os.path import join, dirname, abspath
import time
import sys

class NeuralNetAI(AI):
    name = ''

    def __init__(self, *args, num_players=2, stepsize=0.05, restore=False, prob_factor=1., **kwargs):
        super(NeuralNetAI, self).__init__(*args, **kwargs)
        self.stepsize = stepsize
        self.prob_factor = prob_factor
        self.num_players = num_players
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
            # move = ('gems', {})
            # move_info = MoveInfo(move=move, )
            # return (('gems', {}), np.array([0.5, 0.5]))
            moves = [('gems', {})]


        current_player_index = state.current_player_index
        new_states = [state.copy().make_move(move) for move in moves]
        vectors = np.array([new_state.get_state_vector(current_player_index) for new_state in new_states])
        try:
            probabilities = self.session.run(self.probabilities, {self.input_state: vectors})
        except ValueError:
            print('Error calculating self.probabilities - maybe there are no available moves')
            import ipdb
            ipdb.set_trace()

        probabilities = probabilities

        # player_probabilities = probabilities[state.current_player_index]
        player_probabilities = probabilities[0]

        index = np.random.choice(range(len(moves)), p=player_probabilities)
        choice = moves[index]

        num_players = self.num_players
        new_state = new_states[index]
        player_vecs = np.array([new_state.get_state_vector(i) for i in range(num_players)])
        values = self.session.run(self.softmax_output,
                                  {self.input_state: player_vecs.reshape(num_players, -1)})

        move_info = MoveInfo(move=choice, post_move_values=values,
                             post_move_vecs=player_vecs)
        return choice, move_info

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
        INPUT_SIZE = 347 #297 #345 #249 #265 # 305 # 265 # 585 
        # INPUT_SIZE = 293 # 294 # 613
        HIDDEN_LAYER_SIZE = 20
        HIDDEN_LAYER_SIZE = 50

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
        output = tf.matmul(hidden_output_1, weight_2) + bias_2 * 0.
        softmax_output = tf.nn.softmax(output)

        real_result = tf.placeholder(tf.float32, [None, 2])

        train_step = tf.train.GradientDescentOptimizer(stepsize_variable * stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output)))
        # train_step = tf.train.AdamOptimizer(stepsize_variable * stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output)))

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

        # self.raw_output_rows = tf.transpose(softmax_output)
        # self.row_sums = tf.reduce_sum(self.raw_output_rows, axis=1)
        # self.raw_output_rows = self.raw_output_rows / tf.reshape(self.row_sums, (-1, 1))
        # self.probabilities = tf.nn.softmax(self.raw_output_rows * self.prob_factor)
        self.probabilities = tf.nn.softmax(tf.transpose(softmax_output) * self.prob_factor)

        self.trainable_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
                                                     scope=tf.get_variable_scope().name)
        
    def print_info(self):
        print('weight 1:\n', self.weight_1.eval(self.session))
        print('bias 1:\n', self.bias_1.eval(self.session))
        print('weight 2:\n', self.weight_2.eval(self.session))
        # print('bias 2:\n', self.bias_2.eval(self.session))


class H50AI_TDlam(H50AI):
    name = '2ph50_tdlam'

    def __init__(self, restore=False, **kwargs):
        with tf.variable_scope(self.name):

            super(H50AI_TDlam, self).__init__(**kwargs)

            # self.opt = tf.train.AdamOptimizer()
            # self.opt = tf.train.GradientDescentOptimizer(1.)
            # self.grads = tf.gradients(self.softmax_output[:, 0], self.trainable_variables)
            # self.grads1 = tf.gradients(self.softmax_output[:, 1], self.trainable_variables)
            # self.grads_s = [tf.placeholder(tf.float32, shape=tvar.get_shape(), name='{}{}{}'.format(i,i,i))
            #                 for i, tvar in enumerate(self.trainable_variables)]
            # self.apply_grads = self.opt.apply_gradients(zip(self.grads_s, self.trainable_variables),
            #                                             name='apply_grads')

            # self.train_step = tf.train.GradientDescentOptimizer(self.stepsize_variable * self.stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.real_result, logits=self.output)))
            self.train_step = tf.train.AdamOptimizer(self.stepsize_variable * self.stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.real_result, logits=self.output)))
            tf.global_variables_initializer().run(session=self.session)

        if restore:
            self.load_variables()

    def make_move(self, state):
        index = state.current_player_index
        vec = state.get_state_vector(index).reshape(1, -1)

        vecs = np.array([state.get_state_vector(i) for i in range(self.num_players)]).reshape(self.num_players, -1)

        move, move_info = super(H50AI_TDlam, self).make_move(state)

        move_info.current_player_index = index
        move_info.pre_move_vecs = vecs

        return move, move_info

    def train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        print('ai.train')

        lam_param = 0.7

        for row_index, row in enumerate(training_data):
            winner_index, state_vectors = row
            # import ipdb
            # ipdb.set_trace()
            sys.stdout.write('\rTraining game {} / {}: {} {}'.format(row_index, len(training_data), state_vectors[-1].post_move_values[0].tolist(), winner_index))
            sys.stdout.flush()
            for i, v in enumerate(state_vectors):
                pre_move_vecs = v.pre_move_vecs
                post_move_vecs = v.post_move_vecs
                post_move_values = v.post_move_values

                for player_index in range(self.num_players):
                    pre_move_vec = pre_move_vecs[player_index:player_index+1]
                    post_move_vec = post_move_vecs[player_index:player_index+1]
                    post_move_value = post_move_values[player_index:player_index+1]

                    assert pre_move_vec is not None and post_move_vec is not None and post_move_value is not None
                    # previous_move, previous_value, previous_vec, previous_grads = v
                    for ni, nv in enumerate(state_vectors[i:]):
                        ni += i

                        post_move_vec = nv.post_move_vecs[player_index:player_index+1]
                        post_move_value = nv.post_move_values[player_index:player_index+1]

                        try:
                            post_move_value = post_move_value.reshape((-1, 2))
                        except AttributeError:
                            import traceback
                            traceback.print_exc()
                            import ipdb
                            ipdb.set_trace()

                        difference = ni - i

                        self.session.run(self.train_step, feed_dict={
                            self.input_state: pre_move_vec,
                            self.real_result: post_move_value,
                            self.stepsize_multiplier: stepsize_multiplier, 
                            self.stepsize_variable: stepsize * lam_param**difference,
                            })

            last_move_info = state_vectors[-1]
            # last_state, last_value, last_vec, last_grad = state_vectors[-1]
            for player_index in range(self.num_players):
                assert np.max(last_move_info.post_move_vecs[player_index]) == 1.
                self.session.run(self.train_step, feed_dict={
                    self.input_state: last_move_info.post_move_vecs[player_index].reshape((1, -1)),
                    self.real_result: last_move_info.post_move_values[player_index].reshape((-1, 2)),
                    self.stepsize_multiplier: stepsize_multiplier,
                    self.stepsize_variable: stepsize * 2.,
                    })
            # import ipdb
            # ipdb.set_trace()

            if row_index == 0:
                print('\nExample game:')
                for i, move_info in enumerate(state_vectors):
                    print(i % 2, move_info.move, move_info.post_move_values[0])
                print()
                
        print()

                
    # def old_train(self, training_data, stepsize_multiplier=1., stepsize=0.01):
    #     for winner_index, state_vectors in training_data:
    #         vs = [v[0] for v in state_vectors]
    #         expected_output = np.zeros(2)
    #         expected_output[winner_index] = 1 
    #         for _ in range(10):
    #             try:
    #                 self.session.run(self.train_step, feed_dict={
    #                     self.input_state: np.array(vs),
    #                     self.real_result: np.array([expected_output for _ in vs]),
    #                     self.stepsize_multiplier: stepsize_multiplier, 
    #                     self.stepsize_variable: stepsize,
    #                     })
    #             except ValueError:
    #                 import traceback
    #                 traceback.print_exc()
    #                 import ipdb
    #                 ipdb.set_trace()


class H50AI_TD(H50AI):
    name = '2ph50_td'

    def __init__(self, **kwargs):
        with tf.variable_scope(self.name):

            super(H50AI_TD, self).__init__(**kwargs)

            # self.opt = tf.train.AdamOptimizer()
            self.opt = tf.train.GradientDescentOptimizer(1.)
            self.grads = tf.gradients(self.softmax_output[:, 0], self.trainable_variables)
            self.grads1 = tf.gradients(self.softmax_output[:, 1], self.trainable_variables)
            self.grads_s = [tf.placeholder(tf.float32, shape=tvar.get_shape(), name='{}{}{}'.format(i,i,i))
                            for i, tvar in enumerate(self.trainable_variables)]
            self.apply_grads = self.opt.apply_gradients(zip(self.grads_s, self.trainable_variables),
                                                        name='apply_grads')

            self.train_step = tf.train.GradientDescentOptimizer(self.stepsize_variable * self.stepsize_multiplier).minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.real_result, logits=self.output)))

    def make_move(self, state):
        index = state.current_player_index
        vec = state.get_state_vector(index).reshape(1, -1)
        grads = self.session.run(self.grads, feed_dict={
            self.input_state: vec})
        move, probability = super(H50AI_TD, self).make_move(state)
        # import ipdb
        # ipdb.set_trace()
        # print(move, probability, sum([a * b**2 for a, b in zip(v, range(len(v)))]))
        return move, probability, vec, grads

    def train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        # lambda_param = 0.7

        # traces = [np.zeros(tvar.shape) for tvar in self.trainable_variables]

        print('ai.train')
        # import ipdb
        # ipdb.set_trace()

        for row_index, row in enumerate(training_data):
            sys.stdout.write('\rTraining game {} / {}: {}'.format(row_index, len(training_data), (state_vectors[-1][1], winner_index)))
            sys.stdout.flush()
            winner_index, state_vectors = row
            previous_move, previous_value, previous_vec, previous_grads = state_vectors[0]
            for move, value, vec, grads in state_vectors[1:]:
                value = value.reshape((-1, 2))
                try:
                    delta = value[0] - previous_value[0]
                    delta *= -1**(winner_index)
                    prev_sum = np.sum(np.abs(previous_grads[0]))
                    # previous_grads = self.session.run(self.grads, feed_dict={self.input_state: previous_vec})
                    new_sum = np.sum(np.abs(previous_grads[0]))
                    print('sum diff', new_sum / prev_sum)

                    # feed_dict = {grad_var: -delta * previous_grad * stepsize
                    #             for previous_grad, grad_var in zip(previous_grads, self.grads_s)}
                    # import ipdb
                    # ipdb.set_trace()
                    print([np.sum(g) for g in previous_grads])
                    # self.session.run(self.apply_grads,
                    #                 feed_dict=feed_dict)

                    for _ in range(10):
                        self.session.run(self.train_step, feed_dict={
                            self.input_state: previous_vec,
                            self.real_result: value,
                            self.stepsize_multiplier: stepsize_multiplier, 
                            self.stepsize_variable: stepsize,
                            })
                except (ValueError, IndexError):
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()
                    print('...')

                previous_move = move
                previous_value = value
                previous_grads = grads
                previous_vec = vec
        print()
                
    def old_train(self, training_data, stepsize_multiplier=1., stepsize=0.01):
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
