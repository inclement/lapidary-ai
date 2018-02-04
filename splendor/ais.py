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

from nn import H50AI

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



class GameManager(object):
    def __init__(self, players=2, ais=[], end_score=15, validate=True):
        self.end_score = end_score
        self.num_players = players

        self.validate = validate

        assert len(ais) == players

        self.ais = ais

    def run_game(self, verbose=True):
        state = GameState(players=self.num_players, init_game=True,
                          validate=self.validate)
        self.state = state

        state_vectors = [[] for _ in range(self.num_players)]
        game_round = 0
        state = state
        while True:
            for i, player in enumerate(state.players):
                # if len(player.cards_in_hand) == 3:
                #     if verbose:
                #         print('## player {} wins with 3 cards in hand after {} rounds'.format(i + 1, game_round))
                #     return game_round, i, 0, state_vectors
                    
                if len(player.cards_played) == 1:
                # if player.score >= 3:
                    if verbose:
                        print('## player {} wins with 3 points after {} rounds'.format(i + 1, game_round))
                    winner_num_bought = len(state.players[i].cards_played)
                    return game_round, i, winner_num_bought, state_vectors

            if state.current_player_index == 0:
                game_round += 1
                if verbose:
                    print('Round {}: {}'.format(game_round, state.get_scores()))
            if game_round > 50:
                return game_round, None, None, state_vectors
            # scores = state.get_scores()
            # if any([score >= self.end_score for score in scores]):
            #     break

            # game end

            current_player_index = state.current_player_index
            
            move = self.ais[state.current_player_index].make_move(state)
            if verbose:
                print('P{}: {}'.format(state.current_player_index, move))
            # if move[0] == 'buy_available':
            #     action, tier, index, gems = move
            #     if verbose:
            #         print(state.cards_available_in(tier)[index])
            state.make_move(move)

            new_state_vector = state.get_state_vector(current_player_index)
            state_vectors[current_player_index].append(new_state_vector)

        winner_index = np.argmax(scores)
        if verbose:
            state.print_state()
        print('Ended with scores {} after {} rounds'.format(scores, game_round))

        winner_num_bought = len(state.players[winner_index].cards_played)

        return game_round, winner_index, winner_num_bought, state_vectors

ais = {'nn2ph50': H50AI(),
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

    parser.add_argument('--no-validate', action='store_true', default=False)

    args = parser.parse_args(sys.argv[1:])

    # ais = [H50AI()] + [RandomAI() for _ in range(args.players - 1)]
    ai = H50AI(restore=args.restore, stepsize=args.stepsize, prob_factor=args.prob_factor)
    ais = [ai for _ in range(args.players)]
    # ais = [)] + [RandomAI() for _ in range(args.players - 1)]
    manager = GameManager(players=args.players, ais=ais,
                          end_score=args.end_score,
                          validate=(not args.no_validate))

    if len(glob(join('saves', '{}.*'.format(ai.name)))) and not args.restore:
        print('restore information present but not asked to use')
        exit(1)

    test_state = GameState(players=args.players, init_game=True)
    # test_state.num_red_available -= 1
    # test_state.num_white_available -= 1
    # test_state.num_black_available -= 1
    # test_state.players[0].red += 1
    # test_state.players[0].white += 1
    # test_state.players[0].black += 1
    # p1 = test_state.players[0]
    # for colour in colours:
    #     setattr(p1, colour, 2)
    #     setattr(test_state, 'num_{}_available'.format(colour), 2)
    test_moves = test_state.get_valid_moves(0)
    test_state_vector = test_state.get_state_vector(0)

    # pre-training
    # for _ in range(10000):
    #     ai.session.run(ai.train_step, feed_dict={
    #         ai.input_state: np.array([[0., 1.], [1., 0.]]), ai.real_result: [[1.], [-1.]]})

    # # FAKE TRAINING
    # print('FAKE TRAINING pre')
    # ai.print_info()
    # training_data = []
    # outputs = []
    # state = test_state.copy()
    # state.num_red_available -= 1
    # state.num_white_available -= 1
    # state.num_black_available -= 1
    # state.players[0].red += 1
    # state.players[0].white += 1
    # state.players[0].black += 1
    # vector = state.get_state_vector(0)
    # for _ in range(1):
    #     ai.session.run(ai.train_step, feed_dict={
    #         ai.input_state: np.array([vector for _ in range(1000)]),
    #         ai.real_result: np.array([[1., 0.] for _ in range(1000)]),
    #         ai.stepsize_multiplier: 1.,
    #         ai.stepsize_variable: args.stepsize,
    #         })
    #     # print('======\n')
    #     # ai.print_info()
    # print('FAKE TRAINING post')
    # ai.print_info()


    round_nums = []
    t_before = time.time()
    round_collection = []
    training_data = []
    progress_info = []
    cur_time = time.time()
    try:
        for i in range(args.number):
            if i % args.train_steps == 0:
                new_time = time.time()
                print('======== round {} / {}'.format(i, args.number))
                ai.print_info()
                # print('test output', ai.session.run(ai.output, {ai.input_state: test_state_vector.reshape((1, -1))}))
                new_states = [test_state.copy().make_move(move) for move in test_moves]
                vectors = np.array([new_state.get_state_vector(0) for new_state in new_states])
                outputs = ai.session.run(ai.output, {ai.input_state: vectors})
                probabilities = ai.session.run(ai.probabilities, {ai.input_state: vectors})

                weight_1 = ai.session.run(ai.weight_1)
                bias_1 = ai.session.run(ai.bias_1)
                weight_2 = ai.session.run(ai.weight_2)
                bias_2 = ai.session.run(ai.bias_2)
                # import ipdb
                # ipdb.set_trace()
                # print('test outputs: {:.05f} {:.05f} ({:.03f})'.format(outputs[0], outputs[-1], outputs[-1] / outputs[0]))
                print('test outputs:\n', outputs)
                # print('test moves', test_moves)
                print('test probabilities:')
                for move, prob in zip(test_moves, probabilities[0]):
                    print('{:.05f}% : {}'.format(prob * 100, move))
                if args.debug_after_test:
                    import ipdb
                    ipdb.set_trace()
                round_collection = np.array(round_collection)
                if len(round_collection):
                    progress_info.append(
                        (np.sum(round_collection[:, 1] == 0) / len(round_collection), np.average(round_collection[:, 0]), np.average(round_collection[:, 2]), probabilities[0], weight_1[:, -2:]))
                    print('in last {} rounds, player 1 won {:.02f}%, average length {} rounds'.format(args.train_steps,
                        np.sum(round_collection[:, 1] == 0) / len(round_collection) * 100, np.average(round_collection[:, 0])))
                    print('Game ended in 3 rounds {} times'.format(np.sum(round_collection[:, 0] == 3)))
                    print('Player 1 won in 3 rounds {} times'.format(np.sum((round_collection[:, 0] == 3) & (round_collection[:, 1] == 0))))
                round_collection = []

                print('Time per game: {}'.format((new_time - cur_time) / args.train_steps))
                cur_time = time.time()


            num_rounds, winner_index, winner_num_bought, state_vectors = manager.run_game(verbose=False)
            if winner_index is not None:
                training_data.append((winner_index, state_vectors))
                round_collection.append([num_rounds, winner_index, winner_num_bought])
            if winner_index is None:
                print('Stopped after round 50')
                # continue
            round_nums.append(num_rounds)


            # train the ai
            if i % args.train_steps == 0 and i > 10:
                print('training...', len(training_data))
                for winner_index, state_vectors in training_data:
                    for vi, vs in enumerate(state_vectors):
                        if vi != 0:
                            # print('skipping training from pov of player {}'.format(vi + 1))
                            continue
                        expected_output = np.zeros(2)
                        expected_output[winner_index] = 1 
                        # if winner_index is not None:
                        #     expected_output = 1 if vi == winner_index else 0
                        # else:
                        #     expected_output = 0
                        # print('training as {}'.format(expected_output))
                        # print(np.array(vs))
                        # import ipdb
                        # ipdb.set_trace()
                        for _ in range(10):
                            ai.session.run(ai.train_step, feed_dict={
                                ai.input_state: np.array(vs),
                                ai.real_result: np.array([expected_output for _ in vs]),
                                ai.stepsize_multiplier: 1., 
                                ai.stepsize_variable: args.stepsize,
                                # ai.stepsize_multiplier: np.ones(len(vs)),
                                # ai.stepsize_variable: np.ones(len(vs)) * args.stepsize,
                                })
                training_data = []
                print('done')
            if i % args.train_steps == 0 and i > 10:
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

                ys1 = [i[1] for i in progress_info]
                ax2.plot([i[1] for i in progress_info])
                if len(ys1) > 4:
                    av = rolling_average(ys1)
                    av = np.hstack([[av[0]], [av[0]], av])
                    ax2.plot(np.arange(len(progress_info))[:-2], av)
                ax2.set_xlabel('step')
                ax2.set_ylabel('average length')

                ax3.plot(np.arange(len(progress_info)), [i[3] for i in progress_info])
                ax3.set_xlabel('step')
                ax3.set_ylabel('probabilities')

                ys1 = [i[2] for i in progress_info]
                ax4.plot([i[2] for i in progress_info])
                if len(ys1) > 4:
                    av = rolling_average(ys1)
                    av = np.hstack([[av[0]], [av[0]], av])
                    ax4.plot(np.arange(len(progress_info))[:-2], av)
                ax4.set_xlabel('step')
                ax4.set_ylabel('average winner cards played')
                
                ax5.set_axis_off()
                ax6.set_axis_off()

                fig.set_size_inches((10, 8))
                fig.tight_layout()
                fig.savefig('output.png')
                print('done')
            # import ipdb
            # ipdb.set_trace()
            t_after = time.time()
            # print('dt: {}'.format(t_after - t_before))
            # if i > 50 and (t_after - t_before) > 1.5:
            #     import ipdb
            #     ipdb.set_trace()
            t_before = t_after
            # print('done')
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
