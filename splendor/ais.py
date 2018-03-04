from data import colours
from game import GameState
from aibase import AI

import matplotlib.pyplot as plt

import numpy as np

import argparse
import sys
import time
from glob import glob
from os.path import join

from nn import H50AI, H50AI_TDlam


class RandomAI(AI):
    '''Chooses random moves, with preference given to buying, then
    reserving, then gems.

    '''

    def make_move(self, state):
        moves = state.get_valid_moves(state.current_player_index)
        # return state.generator.choice(moves)

        if state.players[state.current_player_index].num_gems <= 8:
            gems_moves = [move for move in moves if move[0] == 'gems']
            if gems_moves and state.total_num_gems_available() >= 3:
                return state.generator.choice(gems_moves)
                

        buying_moves = [move for move in moves if move[0] == 'buy_available' or move[0] == 'buy_reserved']
        if buying_moves:
            return state.generator.choice(buying_moves)

        reserving_moves = [move for move in moves if move[0] == 'reserve']
        if reserving_moves:
            return state.generator.choice(reserving_moves)

        return state.generator.choice(moves)
      
    def choose_noble(self, state, nobles):
        return state.generator.choice(nobles)


class FinishedGameInfo(object):
    def __init__(self, length, winner_index,
                 winner_num_t1_bought=0,
                 winner_num_t2_bought=0,
                 winner_num_t3_bought=0,
                 state_vectors=[]):
        self.length = length
        self.winner_index = winner_index
        self.winner_num_t1_bought = winner_num_t1_bought
        self.winner_num_t2_bought = winner_num_t2_bought
        self.winner_num_t3_bought = winner_num_t3_bought

        self.state_vectors = state_vectors

    @property
    def winner_num_bought(self):
        return self.winner_num_t1_bought + self.winner_num_t2_bought + self.winner_num_t3_bought


class GameManager(object):
    def __init__(self, players=2, ais=[], end_score=15, validate=True):
        self.end_score = end_score
        self.num_players = players

        self.validate = validate

        assert len(ais) == players

        self.ais = ais

    def run_game(self, verbose=True):
        # print('===')
        state = GameState(players=self.num_players, init_game=True,
                          validate=self.validate)
        self.state = state

        state_vectors = []
        # Add the judgement of the first state vector
        ai = self.ais[0]
        state_vector = state.get_state_vector(0).reshape((1, -1))
        current_value = ai.session.run(ai.softmax_output, {ai.input_state: state_vector})[0]
        # current_grads = ai.session.run(ai.grads, feed_dict={ai.input_state: state_vector})
        # state_vectors.append((state.get_state_vector(0), current_value, state_vector, current_grads))

        game_round = 0
        state = state
        while True:
            for i, player in enumerate(state.players):
                # if len(player.cards_in_hand) == 3:
                #     if verbose:
                #         print('## player {} wins with 3 cards in hand after {} rounds'.format(i + 1, game_round))
                #     return game_round, i, 0, state_vectors
                    
                # if (i == 0 and len(player.cards_played) == 1) or (i == 1 and len(player.cards_in_hand) == 3):
                if player.score >= 3: # and len(player.cards_in_hand) >= 3:
                # if player.score >= 1:
                # if len(player.cards_in_hand) >= 3:
                # if player.num_gems('black') >= 1 and player.num_gems('green') >= 1:
                    if verbose:
                        print('## player {} wins with 3 points after {} rounds'.format(i + 1, game_round))

                    try:
                        state.verify_state()
                    except AssertionError:
                        import traceback
                        traceback.print_exc()
                        import ipdb
                        ipdb.set_trace()

                    # state.state_vector.from_perspective_of(1, debug=True)
                    # import ipdb
                    # ipdb.set_trace()
                    winner_num_bought = len(state.players[i].cards_played)

                    winner_value = np.zeros(self.num_players)
                    winner_value[i] = 1.
                    for player_index in range(state.num_players):
                        # state_vectors[-1].post_move_value[player_index] = (1. if player_index == i else 0.)
                        state_vectors[-1].post_move_values[player_index] = np.roll(winner_value, -1 * player_index)

                    assert ((i + 1) % state.num_players) == state.current_player_index

                    winner_t1 = len([c for c in state.players[i].cards_played if c.tier == 1])
                    winner_t2 = len([c for c in state.players[i].cards_played if c.tier == 2])
                    winner_t3 = len([c for c in state.players[i].cards_played if c.tier == 3])
                    return FinishedGameInfo(game_round, i,
                                            winner_num_t1_bought=winner_t1,
                                            winner_num_t2_bought=winner_t2,
                                            winner_num_t3_bought=winner_t3,
                                            state_vectors=state_vectors)
                    # return game_round, i, winner_num_bought, state_vectors

            if state.current_player_index == 0:
                game_round += 1
                if verbose:
                    print('Round {}: {}'.format(game_round, state.get_scores()))
            if game_round > 50:
                return FinishedGameInfo(None, None, state_vectors=state_vectors)
                # return game_round, None, None, state_vectors
            # scores = state.get_scores()
            # if any([score >= self.end_score for score in scores]):
            #     break

            # game end

            current_player_index = state.current_player_index
            
            move, move_info = self.ais[state.current_player_index].make_move(state)
            # print(state.current_player_index, move, values[:-1])
            if verbose:
                print('P{}: {}, value {}'.format(state.current_player_index, move, values))
            last_player = state.current_player_index
            state.make_move(move)

            # new_state_vector = state.get_state_vector(current_player_index)
            state_vectors.append(move_info)

        winner_index = np.argmax(scores)
        if verbose:
            state.print_state()
        print('Ended with scores {} after {} rounds'.format(scores, game_round))

        winner_num_bought = len(state.players[winner_index].cards_played)

        return game_round, winner_index, winner_num_bought, state_vectors

ais = {'nn2ph50': H50AI(),
       # 'nn2ph50_td': H50AI_TD(),
       'random': H50AI()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=2)
    parser.add_argument('--end-score', type=int, default=15)
    parser.add_argument('--number', type=int, default=1)
    parser.add_argument('--restore', action='store_true', default=False)
    parser.add_argument('--stepsize', type=float, default=0.05)
    parser.add_argument('--debug-after-test', action='store_true', default=False)
    parser.add_argument('--train-steps', type=int, default=500)
    parser.add_argument('--prob-factor', type=float, default=10)
    parser.add_argument('--learning-half-life', type=float, default=0.)
    parser.add_argument('--no-train', default=False, action='store_true')

    parser.add_argument('--no-validate', action='store_true', default=False)

    args = parser.parse_args(sys.argv[1:])

    # ais = [H50AI()] + [RandomAI() for _ in range(args.players - 1)]
    # ai = H50AI(restore=args.restore, stepsize=args.stepsize, prob_factor=args.prob_factor)
    ai = H50AI_TDlam(restore=args.restore, stepsize=args.stepsize, prob_factor=args.prob_factor, num_players=args.players)
    ais = [ai for _ in range(args.players)]
    # ais = [)] + [RandomAI() for _ in range(args.players - 1)]
    manager = GameManager(players=args.players, ais=ais,
                          end_score=args.end_score,
                          validate=(not args.no_validate))

    if len(glob(join('saves', '{}.*'.format(ai.name)))) and not args.restore:
        print('restore information present but not asked to use')
        exit(1)

    import tensorflow as tf
    # ai.session.run(tf.global_variables_initializer())
    # ai.load_variables()

    test_state = GameState(players=args.players, init_game=True)
    test_moves = test_state.get_valid_moves(0)
    test_state_vector = test_state.get_state_vector(0)

    stepsize_multiplier = 1.
    learning_rate_half_life = args.learning_half_life * args.train_steps
    learning_rate_halved_at = []

    round_nums = []
    t_before = time.time()
    round_collection = []
    training_data = []
    progress_info = []
    cur_time = time.time()
    try:
        for i in range(args.number):

            if args.learning_half_life > 0. and i % learning_rate_half_life == 0 and i > 10:
                print('Halving stepsize multiplier')
                stepsize_multiplier /= 2.
                learning_rate_halved_at.append(i / args.train_steps)

            # num_rounds, winner_index, winner_num_bought, state_vectors = manager.run_game(verbose=False)
            game_info = manager.run_game(verbose=False)
            if game_info.winner_index is not None:
                training_data.append((game_info.winner_index, game_info.state_vectors))
                round_collection.append(game_info)
            if game_info.winner_index is None:
                print('Stopped after round 50')
                # continue
            round_nums.append(game_info.length)

            # train the ai
            if i % args.train_steps == 0 and i > 10 and not args.no_train:

                print('training...', len(training_data))
                ai.train(training_data,
                         stepsize_multiplier=stepsize_multiplier,
                         stepsize=args.stepsize)
                training_data = []
                print('done')


            if i % args.train_steps == 0: # This happens even on the first run
                new_time = time.time()
                print('======== round {} / {}'.format(i, args.number))
                ai.print_info()
                new_states = [test_state.copy().make_move(move) for move in test_moves]
                vectors = np.array([new_state.get_state_vector(0) for new_state in new_states])
                outputs = ai.session.run(ai.output, {ai.input_state: vectors})
                softmax_outputs = ai.session.run(ai.softmax_output, {ai.input_state: vectors})
                probabilities = ai.session.run(ai.probabilities, {ai.input_state: vectors})

                weight_1 = ai.session.run(ai.weight_1)
                bias_1 = ai.session.run(ai.bias_1)
                weight_2 = ai.session.run(ai.weight_2)
                bias_2 = ai.session.run(ai.bias_2)
                print('test outputs:')
                for row in zip(outputs, softmax_outputs):
                    print(row[0], row[1])
                print('test probabilities:')
                for move, prob in zip(test_moves, probabilities[0]):
                    print('{:.05f}% : {}'.format(prob * 100, move))
                if args.debug_after_test:
                    import ipdb
                    ipdb.set_trace()
                # round_collection = np.array(round_collection)
                if len(round_collection):
                    progress_info.append((
                        np.average([gi.winner_index == 0 for gi in round_collection]),
                        np.average([gi.length for gi in round_collection]),
                        np.average([gi.winner_num_bought for gi in round_collection]),
                        np.average([gi.winner_num_t1_bought for gi in round_collection]),
                        np.average([gi.winner_num_t2_bought for gi in round_collection]),
                        np.average([gi.winner_num_t3_bought for gi in round_collection]),
                        probabilities[0],
                        np.std([gi.length for gi in round_collection]),
                        [gi.length for gi in round_collection],
                        weight_1[:, -2:]))
                        # (np.sum(round_collection[:, 1] == 0) / len(round_collection), np.average(round_collection[:, 0]), np.average(round_collection[:, 2]), probabilities[0], weight_1[:, -2:]))
                    print('in last {} rounds, player 1 won {:.02f}%, average length {} rounds'.format(
                        args.train_steps,
                        progress_info[-1][0] * 100,
                        progress_info[-1][1]))

                    # print('Game ended in 3 rounds {} times'.format(np.sum(round_collection[:, 0] == 3)))
                    # print('Player 1 won in 3 rounds {} times'.format(np.sum((round_collection[:, 0] == 3) & (round_collection[:, 1] == 0))))
                round_collection = []

                print('Time per game: {}'.format((new_time - cur_time) / args.train_steps))
                cur_time = time.time()
                print('Current learning rate multiplier: {}'.format(stepsize_multiplier))

            if (i % args.train_steps == 0) and (i > 10):
                print('plotting')
                fig, axes = plt.subplots(ncols=3, nrows=2)
                ax1, ax2, ax3 = axes[0]
                ax4, ax5, ax6 = axes[1]

                ys0 = [i[0] for i in progress_info]
                ax1.plot([i[0] for i in progress_info])
                if len(ys0) > 4:
                    av = rolling_average(ys0)
                    av = np.hstack([[av[0]], [av[0]], av])
                    ax1.plot(np.arange(len(progress_info))[:-2], av)
                ax1.set_xlabel('step')
                ax1.set_ylabel('player 1 winrate')
                ax1.set_ylim(0, 1)
                ax1.grid()

                ys1 = np.array([i[1] for i in progress_info])
                stds1 = np.array([i[7] for i in progress_info])
                ax2.plot([i[1] for i in progress_info])
                if len(ys1) > 4:
                    av = rolling_average(ys1)
                    av = np.hstack([[av[0]], [av[0]], av])
                    ax2.plot(np.arange(len(progress_info))[:-2], av)
                ax2.fill_between(np.arange(len(progress_info)), ys1 - stds1, ys1 + stds1, color='C0', alpha=0.3)
                ax2.set_xlabel('step')
                ax2.set_ylabel('average length')
                ax2.grid()

                ax3.plot(np.arange(len(progress_info)), [i[6] for i in progress_info])
                ax3.set_xlabel('step')
                ax3.set_ylabel('probabilities')
                ax3.set_yscale('log')
                ax3.set_ylim(10**-3, 10**0)

                ys1 = [i[2] for i in progress_info]
                ax4.plot([i[2] for i in progress_info])
                if len(ys1) > 4:
                    av = rolling_average(ys1)
                    av = np.hstack([[av[0]], [av[0]], av])
                    ax4.plot(np.arange(len(progress_info))[:-2], av)
                ax4.set_xlabel('step')
                ax4.set_ylabel('average winner cards played')
                ax4.grid()

                ys1 = [i[3] for i in progress_info]
                ax5.plot([i[3] for i in progress_info], label='tier 1')
                ax5.plot([i[4] for i in progress_info], label='tier 2')
                ax5.plot([i[5] for i in progress_info], label='tier 3')
                ax5.set_xlabel('step')
                ax5.set_ylabel('average winner cards played each tier')
                ax5.grid()
                ax5.legend()
                
                num = min(10, len(progress_info) - 1)
                for i in range(num):
                    data = progress_info[-num + i][8]
                    ax6.hist(data, alpha=(i + 1) / 11., normed=True, label='dataset {}'.format(-num + i))
                all_data = np.hstack([row[8] for row in progress_info[-10:]])
                ax6.hist(all_data, color='red', histtype='step', normed=True, label='all', linewidth=2)
                ax6.legend(fontsize=8)
                ax6.set_xlabel('length')
                ax6.set_ylabel('frequency')

                for ax in (ax1, ax2):
                    for number in learning_rate_halved_at:
                        ax.axvline(number, color='black')

                fig.set_size_inches((10, 8))
                fig.tight_layout()
                fig.savefig('output.png')
                print('done')

                # import ipdb
                # ipdb.set_trace()
    except KeyboardInterrupt:
        ai.saver.save(ai.session, ai.ckpt_filen())

    from numpy import average, std
    print('Average number of rounds: {} ± {}'.format(average(round_nums), std(round_nums)))

def rolling_average(ps):
    N  = 5
    cumsum = np.cumsum(np.insert(ps, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
