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
        self.state = GameState(players=players)
        self.end_score = end_score

        assert len(ais) == players

        self.ais = ais

    def run_game(self):
        game_round = 0
        state = self.state
        while True:
            if state.current_player_index == 0:
                game_round += 1
                print('Round {}: {}'.format(game_round, state.get_scores()))
            scores = self.state.get_scores()
            if any([score >= self.end_score for score in scores]):
                break

            move = self.ais[self.state.current_player_index].make_move(self.state)
            print('P{}: {}'.format(self.state.current_player_index, move))
            if move[0] == 'buy_available':
                action, tier, index, gems = move
                print(self.state.cards_available_in(tier)[index])
            self.state.make_move(move)

        state.print_state()
        print('Ended with scores', scores)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=2)
    parser.add_argument('--end_score', type=int, default=15)

    args = parser.parse_args(sys.argv[1:])

    manager = GameManager(players=args.players, ais=[RandomAI() for _ in range(args.players)])

    manager.run_game()

if __name__ == "__main__":
    main()
