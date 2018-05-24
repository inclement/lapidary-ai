

from aibase import AI, MoveInfo

import tensorflow as tf
import numpy as np

from data import colours

from os.path import join, dirname, abspath
import time
import sys
from collections import defaultdict

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

    def make_move(self, state, depth=1, move_choice='softmax'):
        moves = state.get_valid_moves(state.current_player_index)

        current_player_index = state.current_player_index
        new_states = [state.copy().make_move(move) for move in moves]

        # if depth > 0:
        #     new_states = [state.make_move(self.make_move(state, depth=depth-1)[0])
        #                   for state in new_states]

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

        # if depth > 0 and np.sum(player_probabilities > 0) >= 5:
        #     best_moves = np.random.choice(range(len(moves)), p=player_probabilities,
        #                                   size=min(5, len(moves), np.sum(player_probabilities > 0)),
        #                                   replace=False)
        #     new_states = [new_states[i] for i in best_moves]
        #     moves = [moves[i] for i in best_moves]
        #     rec_new_states = [state.copy().make_move(self.make_move(state, depth=depth-1, move_choice='max')[0])
        #                       for state in new_states]
        #     rec_vectors = np.array([rec_new_state.get_state_vector(current_player_index)
        #                             for rec_new_state in rec_new_states])
        #     probabilities= self.session.run(self.probabilities, {self.input_state: rec_vectors})
        #     player_probabilities = probabilities[0]

        scores = [state.players[current_player_index].score for state in new_states]
        if np.max(scores) >= 15:
            index = np.argmax(scores)
        elif move_choice == 'softmax':
            index = np.random.choice(range(len(moves)), p=player_probabilities)
        elif move_choice == 'max':
            index = np.argmax(player_probabilities)
        else:
            raise ValueError('Unrecognised move_choice {}'.format(move_choice))
        choice = moves[index]

        num_players = self.num_players
        new_state = new_states[index]
        player_vecs = np.array([new_state.get_state_vector(i) for i in range(num_players)])
        values = self.session.run(self.softmax_output,
                                  {self.input_state: player_vecs.reshape(num_players, -1)})

        move_info = MoveInfo(move=choice, post_move_values=values,
                             post_move_vecs=player_vecs,
                             post_move_scores=[player.score for player in new_state.players],
                             post_move_cards_each_tier=[player.num_cards_each_tier
                                                        for player in new_state.players],
                             post_move_num_gems_in_supply=new_state.total_num_gems_available())
        return choice, move_info

    def evaluate(self, state):
        player_vecs = np.array([state.get_state_vector(i) for i in range(self.num_players)])
        values = self.session.run(self.softmax_output,
                                  {self.input_state: player_vecs.reshape(self.num_players, -1)})

        return values

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
        INPUT_SIZE = 2170 # 1022 #987 #935 #986 #818 #767 #647 #479 #647 #563 #479 #395 #647 # 395 #407 #297 #345 #249 #265 # 305 # 265 # 585 
        # INPUT_SIZE = 293 # 294 # 613
        HIDDEN_LAYER_SIZE = 50
        HIDDEN_LAYER_SIZE = 100

        input_state = tf.placeholder(tf.float32, [None, INPUT_SIZE], name='input_state')
        weight_1 = tf.Variable(tf.truncated_normal([INPUT_SIZE, HIDDEN_LAYER_SIZE], stddev=0.1),
                               name='weight_1')
        bias_1 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE], stddev=0.1),
                             name='bias_1')

        # output = tf.matmul(input_state, weight_1) + bias_1

        self.intermediate_1 = tf.matmul(input_state, weight_1);
        hidden_output_1 = tf.nn.relu(tf.matmul(input_state, weight_1) + bias_1)

        # Hidden layers
        hidden_output_i = hidden_output_1
        for i in range(0):
            weight_i = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE], stddev=0.1),
                                name='weight_2')
            bias_i = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE], stddev=0.1),
                                name='bias_2')

            hidden_output_i = tf.nn.relu(tf.matmul(hidden_output_i, weight_i) + bias_i)
        hidden_output_1 = hidden_output_i

        # Output layer
        weight_2 = tf.Variable(tf.truncated_normal([HIDDEN_LAYER_SIZE, 2], stddev=0.1),
                               name='weight_2')
        bias_2 = tf.Variable(tf.truncated_normal([2], stddev=0.1),
                             name='bias_2')

        stepsize_variable = tf.placeholder(tf.float32, shape=[], name='stepsize')
        stepsize_multiplier = tf.placeholder(tf.float32, shape=[], name='stepsize_multiplier')

        # output = tf.matmul(hidden_output_m, weight_2) + bias_2 
        # output = tf.matmul(hidden_output_m2, weight_2) + bias_2 
        self.intermediate_2 = tf.matmul(hidden_output_1, weight_2);
        output = tf.matmul(hidden_output_1, weight_2) + bias_2 
        softmax_output = tf.nn.softmax(output)

        real_result = tf.placeholder(tf.float32, [None, 2], name='real_result')

        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=real_result, logits=output))
        # train_step = tf.train.GradientDescentOptimizer(stepsize_variable * stepsize_multiplier).minimize(loss)
        session = tf.Session()


        accuracy = tf.reduce_mean((real_result - output)**2)

        self.input_state = input_state
        self.output = output
        self.softmax_output = softmax_output
        self.real_result = real_result
        self.session = session
        self.loss = loss
        self.accuracy = accuracy

        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.bias_1 = bias_1
        self.bias_2 = bias_2
        self.hidden_output_1 = hidden_output_1

        self.stepsize_variable = stepsize_variable
        self.stepsize_multiplier = stepsize_multiplier

        optimizer = tf.train.AdamOptimizer(self.stepsize_variable * self.stepsize_multiplier)
        train_step = optimizer.minimize(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.real_result, logits=self.output)))
        self.optimizer = optimizer
        self.train_step = train_step

        self.saver = tf.train.Saver()


        tf.global_variables_initializer().run(session=session)



        # self.raw_output_rows = tf.transpose(softmax_output)
        # self.row_sums = tf.reduce_sum(self.raw_output_rows, axis=1)
        # self.raw_output_rows = self.raw_output_rows / tf.reshape(self.row_sums, (-1, 1))
        # self.probabilities = tf.nn.softmax(self.raw_output_rows * self.prob_factor)
        self.probabilities = tf.nn.softmax(tf.transpose(softmax_output) * self.prob_factor)
        # self.unnormed_outputs = tf.nn.softmax(softmax_output * self.prob_factor)
        # self.norm_factor = tf.sqrt(tf.reduce_sum(self.unnormed_outputs**2, axis=0))
        # self.probabilities = tf.nn.softmax(
        #     tf.transpose(self.unnormed_probabilities * tf.diag(1. / norm_factor) * self.prob_factor))


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

            self.grads = self.optimizer.compute_gradients(self.loss, self.trainable_variables)
            self.grads_s = [tf.placeholder(tf.float32, shape=tvar.get_shape(), name='{}{}{}'.format(i,i,i))
                            for i, tvar in enumerate(self.trainable_variables)]
            self.apply_grads = self.optimizer.apply_gradients(
                zip(self.grads_s, self.trainable_variables),
                name='apply_grads')

            tf.global_variables_initializer().run(session=self.session)

        if restore:
            self.load_variables()

    def make_move(self, state, **kwargs):
        index = state.current_player_index
        vec = state.get_state_vector(index).reshape(1, -1)

        vecs = np.array([state.get_state_vector(i) for i in range(self.num_players)]).reshape(self.num_players, -1)

        move, move_info = super(H50AI_TDlam, self).make_move(state, **kwargs)

        move_info.current_player_index = index
        move_info.pre_move_vecs = vecs

        # DO NOT CALCULATE GRADS HERE
        # grads = [self.session.run(self.grads, feed_dict={
        #     self.input_state: vec.reshape([1, -1]),
        #     self.real_result: real_result.reshape([1, 2])}) for vec, real_result in zip(move_info.pre_move_vecs,
        #                                                                 move_info.post_move_values)]
        # move_info.pre_move_grads = grads

        return move, move_info

    def manual_grads_train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        print('ai.train')

        lam_param = 0.7

        for row_index, row in enumerate(training_data):
            winner_index, state_vectors = row
            sys.stdout.write('\rTraining game {} / {}: {} {}'.format(row_index, len(training_data), state_vectors[-1].post_move_values[0].tolist(), winner_index))
            sys.stdout.flush()

            grads_trace = state_vectors[0].pre_move_grads
            grads_trace = []
            # import ipdb
            # ipdb.set_trace()
            for player_grads in state_vectors[0].pre_move_grads:
                l = []
                for grad in player_grads:
                    l.append((np.zeros(grad[0].shape, dtype=np.float32), ))
                grads_trace.append(l)

            for i, v in enumerate(state_vectors):
                pre_move_vecs = v.pre_move_vecs
                post_move_vecs = v.post_move_vecs
                post_move_values = v.post_move_values

                # pre_move_grads = v.pre_move_grads
                move_info = v
                pre_move_grads = [self.session.run(self.grads, feed_dict={
                    self.input_state: vec.reshape([1, -1]),
                    self.real_result: real_result.reshape([1, 2])}) for vec, real_result in zip(move_info.pre_move_vecs,
                                                                                move_info.post_move_values)]

                for player_index in range(self.num_players):
                    for gi, grad in enumerate(grads_trace[player_index]):
                        grad = grad[0]
                        grad *= lam_param
                        grad += pre_move_grads[player_index][gi][0]

                for player_index in range(self.num_players):
                    player_grads = grads_trace[player_index]
                    feed_dict={
                        grad_: player_grad[0] for grad_, player_grad in zip(self.grads_s, player_grads)}
                    feed_dict[self.stepsize_multiplier] = stepsize_multiplier
                    feed_dict[self.stepsize_variable] = stepsize
                    # import ipdb
                    # ipdb.set_trace()
                    self.session.run(
                        self.apply_grads,
                        feed_dict=feed_dict)

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

            if row_index == 0:
                print('\nExample game:')
                for i, move_info in enumerate(state_vectors):
                    print(i % 2, move_info.move, [m for m in move_info.post_move_values])
                print()
        print()


    def pre_order_train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        print('ai.train')

        lam_param = 0.7

        for row_index, row in enumerate(training_data):
            winner_index, state_vectors = row
            sys.stdout.write('\rTraining game {} / {}: {} {}'.format(row_index, len(training_data), state_vectors[-1].post_move_values[0].tolist(), winner_index))
            sys.stdout.flush()

            # stepsize_trainings = defaultdict(lambda: ([], []))
            for i, v in enumerate(state_vectors):
                pre_move_vecs = v.pre_move_vecs
                post_move_vecs = v.post_move_vecs
                post_move_values = v.post_move_values

                for player_index in range(self.num_players):
                    pre_move_vec = pre_move_vecs[player_index:player_index+1]
                    post_move_vec = post_move_vecs[player_index:player_index+1]
                    post_move_value = post_move_values[player_index:player_index+1]

                    cur_pre_move_vec = pre_move_vec

                    assert pre_move_vec is not None and post_move_vec is not None and post_move_value is not None
                    # previous_move, previous_value, previous_vec, previous_grads = v
                    for ni, nv in enumerate(state_vectors[:i + 1]):

                        post_move_vec = nv.post_move_vecs[player_index:player_index+1]
                        # post_move_value = nv.post_move_values[player_index:player_index+1]

                        pre_move_vec = nv.pre_move_vecs[player_index:player_index + 1]


                        difference = i - ni
                        if difference > 17:
                            continue

                        if difference == 0:
                            assert np.isclose(np.sum(pre_move_vec - cur_pre_move_vec)**2, 0)

                        # cur_stepsize = stepsize * lam_param**difference
                        # stepsize_trainings[cur_stepsize][0].append(pre_move_vec)
                        # stepsize_trainings[cur_stepsize][1].append(post_move_value)
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
                # cur_stepsize = stepsize * 2.
                # stepsize_trainings[cur_stepsize][0].append(last_move_info.post_move_vecs[player_index].reshape((1, -1)))
                # stepsize_trainings[cur_stepsize][1].append(last_move_info.post_move_values[player_index].reshape((-1, 2)))
                self.session.run(self.train_step, feed_dict={
                    self.input_state: last_move_info.post_move_vecs[player_index].reshape((1, -1)),
                    self.real_result: last_move_info.post_move_values[player_index].reshape((-1, 2)),
                    self.stepsize_multiplier: stepsize_multiplier,
                    self.stepsize_variable: stepsize * 2.,
                    })

            # for key, value in stepsize_trainings.items():
            #     pre_move_vecs, post_move_values = value
            #     self.session.run(self.train_step, feed_dict={
            #         self.input_state: np.vstack(pre_move_vecs),
            #         self.real_result: np.vstack(post_move_values),
            #         self.stepsize_multiplier: stepsize_multiplier,
            #         self.stepsize_variable: key,
            #         })

            if row_index == 0:
                print('\nExample game:')
                for i, move_info in enumerate(state_vectors):
                    print(i % 2, move_info.move, move_info.post_move_values[0])
                print()
        print()


    def train(self, training_data, stepsize_multiplier=1., stepsize=0.01):

        print('ai.train')

        lam_param = 0.05

        for row_index, row in enumerate(training_data):
            winner_index, state_vectors = row
            sys.stdout.write('\rTraining game {} / {}: {} {}'.format(row_index, len(training_data), state_vectors[-1].post_move_values[0].tolist(), winner_index))
            sys.stdout.flush()

            # stepsize_trainings = defaultdict(lambda: ([], []))
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
                        if difference > 17:
                            continue

                        # cur_stepsize = stepsize * lam_param**difference
                        # stepsize_trainings[cur_stepsize][0].append(pre_move_vec)
                        # stepsize_trainings[cur_stepsize][1].append(post_move_value)
                        self.session.run(self.train_step, feed_dict={
                            self.input_state: pre_move_vec,
                            self.real_result: post_move_value,
                            self.stepsize_multiplier: stepsize_multiplier, 
                            self.stepsize_variable: stepsize * lam_param**difference,
                            })

            # Train states towards one another
            for i, v in enumerate(state_vectors):
                input_states = v.post_move_vecs
                real_values = v.post_move_values
                assert len(input_states) == 2  # This code currently only works properly with 2 players

                values = np.roll(real_values, 1, axis=0)
                values = np.roll(values, 1, axis=1)

                # import ipdb
                # ipdb.set_trace()

                self.session.run(self.train_step, feed_dict={
                    self.input_state: input_states,
                    self.real_result: values,
                    self.stepsize_multiplier: stepsize_multiplier,
                    self.stepsize_variable: stepsize,
                    })

            last_move_info = state_vectors[-1]
            # last_state, last_value, last_vec, last_grad = state_vectors[-1]
            for player_index in range(self.num_players):
                assert np.max(last_move_info.post_move_vecs[player_index]) == 1.
                # cur_stepsize = stepsize * 2.
                # stepsize_trainings[cur_stepsize][0].append(last_move_info.post_move_vecs[player_index].reshape((1, -1)))
                # stepsize_trainings[cur_stepsize][1].append(last_move_info.post_move_values[player_index].reshape((-1, 2)))
                self.session.run(self.train_step, feed_dict={
                    self.input_state: last_move_info.post_move_vecs[player_index].reshape((1, -1)),
                    self.real_result: last_move_info.post_move_values[player_index].reshape((-1, 2)),
                    self.stepsize_multiplier: stepsize_multiplier,
                    self.stepsize_variable: stepsize * 2.,
                    })

            # for key, value in stepsize_trainings.items():
            #     pre_move_vecs, post_move_values = value
            #     self.session.run(self.train_step, feed_dict={
            #         self.input_state: np.vstack(pre_move_vecs),
            #         self.real_result: np.vstack(post_move_values),
            #         self.stepsize_multiplier: stepsize_multiplier,
            #         self.stepsize_variable: key,
            #         })

            if row_index == 0:
                print('\nExample game:')
                for i, move_info in enumerate(state_vectors):
                    print(i % 2, move_info.move, move_info.post_move_values[0])
                print()
        print()


                
                
                
                
