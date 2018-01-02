from data import colours

class AI(object):

    def create_neural_net(self):
        raise NotImplementedError()

    def make_move(self, state):
        pass


    def choose_noble(self, nobles):
        raise NotImplementedError()
        return nobles[0]


class RandomAI(AI):

    def make_move(self, state):
        moves = self.get_valid_moves(state)

        return state.generator.choice(moves)
      
    def choose_noble(self, state, nobles):
        return state.generator.choice(nobles)
