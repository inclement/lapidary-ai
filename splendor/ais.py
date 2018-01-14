from data import colours
from game import GameState
from aibase import AI

import numpy as np

import argparse
import sys
import time

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
    def __init__(self, players=2, ais=[], end_score=15):
        self.end_score = end_score
        self.num_players = players

        assert len(ais) == players

        self.ais = ais

    def run_game(self, verbose=True):
        state = GameState(players=self.num_players)
        self.state = state

        state_vectors = [[] for _ in range(self.num_players)]
        game_round = 0
        state = state
        while True:
            if state.current_player_index == 0:
                game_round += 1
                if verbose:
                    print('Round {}: {}'.format(game_round, state.get_scores()))
            if game_round > 50:
                return game_round, None, state_vectors
            scores = state.get_scores()
            # if any([score >= self.end_score for score in scores]):
            #     break

            for i, player in enumerate(state.players):
                if len(player.cards_played) == 1:
                    if verbose:
                        print('## player {} wins with 1 card played after {} rounds'.format(i + 1, game_round))
                    return game_round, i, state_vectors

            current_player_index = state.current_player_index
            
            move = self.ais[state.current_player_index].make_move(state)
            if verbose:
                print('P{}: {}'.format(state.current_player_index, move))
            if move[0] == 'buy_available':
                action, tier, index, gems = move
                if verbose:
                    print(state.cards_available_in(tier)[index])
            state.make_move(move)

            new_state_vector = state.get_state_vector(current_player_index)
            state_vectors[current_player_index].append(new_state_vector)

        winner_index = np.argmax(scores)
        if verbose:
            state.print_state()
        print('Ended with scores {} after {} rounds'.format(scores, game_round))

        return game_round, winner_index, state_vectors

ais = {'nn2ph50': H50AI(),
       'random': H50AI()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=2)
    parser.add_argument('--end-score', type=int, default=15)
    parser.add_argument('--number', type=int, default=1)

    args = parser.parse_args(sys.argv[1:])

    # ais = [H50AI()] + [RandomAI() for _ in range(args.players - 1)]
    ai = H50AI()
    ais = [ai for _ in range(args.players)]
    # ais = [)] + [RandomAI() for _ in range(args.players - 1)]
    manager = GameManager(players=args.players, ais=ais,
                          end_score=args.end_score)

    test_state = GameState(players=args.players)
    test_moves = test_state.get_valid_moves(0)
    test_state_vector = test_state.get_state_vector(0)

    # pre-training
    # for _ in range(10000):
    #     ai.session.run(ai.train_step, feed_dict={
    #         ai.input_state: np.array([[0., 1.], [1., 0.]]), ai.real_result: [[1.], [-1.]]})

    round_nums = []
    t_before = time.time()
    round_collection = []
    for i in range(args.number):
        if i % 50 == 0:
            print('======== round {} / {}'.format(i, args.number))
            ai.print_info()
            # print('test output', ai.session.run(ai.output, {ai.input_state: test_state_vector.reshape((1, -1))}))
            new_states = [test_state.copy().make_move(move) for move in test_moves]
            vectors = np.array([new_state.get_state_vector(0) for new_state in new_states])
            outputs = ai.session.run(ai.output, {ai.input_state: vectors}).reshape([-1])
            probabilities = ai.session.run(ai.probabilities, {ai.input_state: vectors})
            # print('test outputs: {:.05f} {:.05f} ({:.03f})'.format(outputs[0], outputs[-1], outputs[-1] / outputs[0]))
            print('test outputs:', *['{:.03f}'.format(v) for v in (outputs / np.sum(outputs))])
            # print('test moves', test_moves)
            print('test probabilities:')
            for move, prob in zip(test_moves, probabilities):
                print('{:.05f}% : {}'.format(prob * 100, move))
            # import ipdb
            # ipdb.set_trace()
            round_collection = np.array(round_collection)
            if len(round_collection):
                print('in last 50 rounds, player 1 won {:.02f}%, average length {} rounds'.format(
                    np.sum(round_collection[:, 1] == 0) / len(round_collection) * 100, np.average(round_collection[:, 0])))
            round_collection = []

        num_rounds, winner_index, state_vectors = manager.run_game(verbose=False)
        round_collection.append([num_rounds, winner_index])
        if winner_index is None:
            print('Stopped after round 50')
            # continue
        round_nums.append(num_rounds)

        # training_data = []
        # outputs = []
        # for num_gems in range(10):
        #     training_data.append([num_gems / 10, 0])
        #     outputs.append(-1)
        # for num_cards in range(3):
        #     training_data.append([0, num_cards / 3.])
        #     outputs.append(1)
        # for _ in range(100):
        #     ai.session.run(ai.train_step, feed_dict={
        #         ai.input_state: np.array(training_data),
        #         ai.real_result: np.array(outputs).reshape((-1, 1))
        #         })
            # print('======\n')
            # ai.print_info()
                        

        # train the ai
        # print('training')
        for vi, vs in enumerate(state_vectors):
            if vi != 0:
                # print('skipping training from pov of player {}'.format(vi + 1))
                continue
            if winner_index is not None:
                expected_output = 1 if vi == winner_index else -1
            else:
                expected_output = 0
            # print('training as {}'.format(expected_output))
            # print(np.array(vs))
            for _ in range(10):
                ai.session.run(ai.train_step, feed_dict={
                    ai.input_state: np.array(vs), ai.real_result: np.array([expected_output for _ in vs]).reshape((-1, 1))
                    })
        # import ipdb
        # ipdb.set_trace()
        t_after = time.time()
        # print('dt: {}'.format(t_after - t_before))
        # if i > 50 and (t_after - t_before) > 1.5:
        #     import ipdb
        #     ipdb.set_trace()
        t_before = t_after
        # print('done')

    from numpy import average, std
    print('Average number of rounds: {} ± {}'.format(average(round_nums), std(round_nums)))

if __name__ == "__main__":
    main()
