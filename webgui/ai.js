


class RandomAI {
    make_move(state) {
        var choice;
        let moves = state.get_valid_moves();
        let player = state.players[state.current_player_index];

        if (player.total_num_gems() <= 8) {
            let gems_moves = [];
            for (let move of moves) {
                if (move['action'] === 'gems') {
                    gems_moves.push(move);
                }
            }
            if (gems_moves.length > 0 && state.total_num_gems_available() >= 3) {
                choice = math.pickRandom(gems_moves);
                return choice;
            }
        }

        let buying_moves = [];
        for (let move of moves) {
            if (move['action'] === 'buy_available' || move['action'] === 'buy_reserved') {
                buying_moves.push(move);
            }
        }
        if (buying_moves.length > 0) {
            choice = math.pickRandom(buying_moves);
            return choice
        }

        let reserving_moves = [];
        for (let move of moves) {
            if (move['action'] === 'reserve') {
                reserving_moves.push(move);
            }
        }
        if (reserving_moves.length > 0) {
            choice = math.pickRandom(reserving_moves);
            return choice;
        }

        return math.pickRandom(moves);
    }
}
