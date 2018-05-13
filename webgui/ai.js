


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

function relu(arr) {
    for (let row_index = 0; row_index < arr.size()[0]; row_index++) {
        let row = arr._data[row_index];
        for (let i = 0; i < row.length; i++) {
            let value = row[i];
            if (value < 0) {
                row[i] = 0;
            }
        }
    }
    return arr;
}

function softmax(arr, prob_factor = 1) {
    let exp_arr = [];
    for (let row of arr) {
        let sum = 0;
        let exp_row = [];
        for (let value of row) {
            let exp_value = Math.exp(prob_factor * value);
            sum += exp_value;
            exp_row.push(exp_value);
        }
        for (let i = 0; i < row.length; i++) {
            exp_row[i] /= sum;
        }
        exp_arr.push(exp_row);
    }
    return exp_arr;
}

class NeuralNetAI {
    constructor() {
        this.weight_1 = math.matrix(weights['weight_1']);
        this.weight_2 = math.matrix(weights['weight_2']);
        this.bias_1 = math.matrix(weights['bias_1']);
        this.bias_2 = math.matrix(weights['bias_2']);

        this.prob_factor = 100;
    }

    make_move(state) {
        let moves = state.get_valid_moves();
        let player = state.players[state.current_player_index];
        let current_player_index = state.current_player_index;

        let input_vector = [];
        let scores = [];
        for (let move of moves) {
            let cur_state = state.copy();
            cur_state.make_move(move);
            input_vector.push(cur_state.get_state_vector(current_player_index));
            scores.push(cur_state.players[current_player_index].score);
        }

        // If we can get to 15 points, do so
        let best_score = 0;
        let best_index = 0;
        for (let i = 0; i < moves.length; i++) {
            let score = scores[i];
            if (score > best_score) {
                best_score = score;
                best_index = i;
            }
        }
        if (best_score >= 15) {
            return moves[best_index]
        }

        // console.log('Using fake input vector');
        // input_vector = vectors;

        // console.log('pre', math.matrix(input_vector), this.weight_1);

        let hidden_output_1 = math.multiply(
            math.matrix(input_vector), this.weight_1);
        // console.log('first multiply', hidden_output_1);
        let bias_1_arr = [];
        for (let i = 0; i < hidden_output_1.size()[0]; i++) {
            bias_1_arr.push(this.bias_1._data);
        }
        hidden_output_1 = math.add(hidden_output_1, bias_1_arr);
    
        // console.log('before relu', hidden_output_1);
        hidden_output_1 = relu(hidden_output_1);
        // console.log('after relu', hidden_output_1);

        hidden_output_1 = math.matrix(hidden_output_1);

        let output = math.multiply(
            hidden_output_1, this.weight_2);
        // console.log('intermediate 2', output);
        let bias_2_arr = [];
        for (let i = 0; i < hidden_output_1.size()[0]; i++) {
            bias_2_arr.push(this.bias_2._data);
        }
        output = math.add(output, bias_2_arr);
        output = softmax(output._data);

        let probabilities_input = [];
        for (let row of output) {
            probabilities_input.push(row[0]);
        }
        let probabilities = softmax([probabilities_input], 100)[0];

        let number = math.random();
        let move = null;
        let cumulative_probability = 0;
        for (let i = 0; i < probabilities.length; i++) {
            cumulative_probability += probabilities[i];
            if (cumulative_probability > number) {
                move = moves[i];
                break;
            }
        }
        if (move === null) {
            console.log('Failed to choose a move using softmax probabilities')
            move = moves[moves.length - 1];
        }

        return move;

    }
}

ai = new NeuralNetAI();
