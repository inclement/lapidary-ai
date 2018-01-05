from data import colours
from game import GameState

import argparse
import sys

class AI(object):

    def create_neural_net(self):
        raise NotImplementedError()

    def make_move(self, state):
        pass


    def choose_noble(self, nobles):
        raise NotImplementedError()
        return nobles[0]


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

        game_round = 0
        state = state
        while True:
            if state.current_player_index == 0:
                game_round += 1
                if verbose:
                    print('Round {}: {}'.format(game_round, state.get_scores()))
            scores = state.get_scores()
            if any([score >= self.end_score for score in scores]):
                break

            move = self.ais[state.current_player_index].make_move(state)
            if verbose:
                print('P{}: {}'.format(state.current_player_index, move))
            if move[0] == 'buy_available':
                action, tier, index, gems = move
                if verbose:
                    print(state.cards_available_in(tier)[index])
            state.make_move(move)

        if verbose:
            state.print_state()
        print('Ended with scores {} after {} rounds'.format(scores, game_round))

        return game_round


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=2)
    parser.add_argument('--end-score', type=int, default=15)
    parser.add_argument('--number', type=int, default=1)

    args = parser.parse_args(sys.argv[1:])

    manager = GameManager(players=args.players, ais=[RandomAI() for _ in range(args.players)],
                          end_score=args.end_score)

    round_nums = []
    for i in range(args.number):
        round_nums.append(manager.run_game(verbose=False))

    from numpy import average, std
    print('Average number of rounds: {} ± {}'.format(average(round_nums), std(round_nums)))

if __name__ == "__main__":
    main()
