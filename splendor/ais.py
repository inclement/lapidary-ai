from data import colours
from itertools import permutations

class AI(object):

    def create_neural_net(self):
        raise NotImplementedError()

    def make_move(self, state):
        pass

    def get_valid_moves(self, state):

        moves = []
        player = state.current_player

        # Moves that take gems
        # 1) taking two of the same colour
        for colour in colours:
            if state.num_gems_available(colour) >= 4:
                moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [c for c in colours if state.num_gems_available(colour) > 0]
        for ps in permutations(available_colours, len(available_colours)):
            ps = ps[:3]  # take only up to 3 gems
            moves.append(('gems', {p: 1 for p in ps}))

        # Moves that buy available cards
        for tier in range(1, 4):
            for index, card in enumerate(state.cards_available_in(tier)):
                can_afford, cost = player.can_afford(card)
                if not can_afford:
                    continue
                moves.append(('buy_available', tier, index, {c: -1 * v for c, v in cost.items()}))

        # Moves that buy reserved cards
        for index, card in enumerate(player.cards_in_hand):
            can_afford, cost = player.can_afford(card)
            if not can_afford:
                continue
            moves.append(('buy_reserved', index, {c: -1 * v for c, v in cost.items()}))

        # Moves that reserve cards
        if player.num_reserved < 3:
            gold_gained = 1 if state.num_gold_available > 0 else 0
            for tier in range(1, 4):
                for i in range(4):
                    moves.append(('reserve', tier, i, {'gold': gold_gained}))
                moves.append(('reserve', tier, -1, {'gold': gold_gained}))
        

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        for move in moves:
            if move[0] == 'gems':
                pass  # discard if necessary
            elif move[0] == 'reserve':
                pass  # discard if necessary

        return moves

    def choose_noble(self, nobles):
        raise NotImplementedError()
        return nobles[0]


class RandomAI(AI):

    def make_move(self, state):
        moves = self.get_valid_moves(state)

        return state.generator.choice(moves)
      
    def choose_noble(self, state, nobles):
        return state.generator.choice(nobles)
