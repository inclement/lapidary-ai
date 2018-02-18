
class AI(object):

    def create_neural_net(self):
        raise NotImplementedError()

    def make_move(self, state):
        pass


    def choose_noble(self, nobles):
        raise NotImplementedError()
        return nobles[0]

class MoveInfo(object):
    def __init__(self,
                 move,
                 pre_move_value=None,
                 post_move_value=None,
                 pre_move_vec=None,
                 post_move_vec=None,
                 current_player_index=None,
                 pre_move_vec_cur_player_pov=None):
        self.move = move

        self.pre_move_value = pre_move_value
        self.post_move_value = post_move_value

        self.pre_move_vec = pre_move_vec
        self.post_move_vec = post_move_vec

        self.pre_move_vec_cur_player_pov = pre_move_vec_cur_player_pov
