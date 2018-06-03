
function state_vector_v01(state, index) {
    let num_players = state.num_players;
    let num_cards = state.num_cards;

    let player_indices = [];
    for (let i = 0; i < num_players; i++) {
        player_indices.push((i + index) % num_players);
    }

    let cur_index = 0;
    let state_components = [];
    var arr;

    // store numbers of gems in the supply
    let num_colour_gems_in_play = state.num_gems_in_play;
    for (let colour of colours) {
        arr = zeros(num_colour_gems_in_play + 1);
        arr[state.supply_gems[colour]] = 1;
        state_components.push(arr);
    }
    // ...plus gold
    arr = zeros(6);
    arr[state.supply_gems['gold']] = 1;
    state_components.push(arr);

    // console.log('first player gem', concatenated(state_components).length);

    // store numbers of gems held by each player
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        for (let colour of colours) {
            arr = zeros(num_colour_gems_in_play + 1);
            arr[player.gems[colour]] = 1;
            state_components.push(arr)
        }
        arr = zeros(6);
        arr[player.gems['gold']] = 1;
        state_components.push(arr);
    }

    // console.log('first coloured card', concatenated(state_components).length);

    // store numbers of coloured cards played by each player
    // only count up to 7 - more than this makes no difference
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        for (let colour of colours) {
            arr = zeros(8);
            arr[Math.min(player.card_colours[colour], 7)] = 1;
            state_components.push(arr);
        }
    }

    // console.log('p0 points', concatenated(state_components).length);

    // store number of points of each player
    // only count up to 20, higher scores are very unlikely
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        arr = zeros(21);
        for (let i = 0; i < Math.min(player.score + 1, 21); i++) {
            arr[i] = 1;
        }
        // arr[Math.min(player.score, 20)] = 1;
        state_components.push(arr);
    }

    // console.log('current player 0', concatenated(state_components).length);

    // store current player
    arr = zeros(num_players);
    current_index = state.current_player_index;
    current_index -= index;
    if (current_index < 0) {
        current_index += state.num_players;
    }
    arr[current_index] = 1;
    state_components.push(arr);

    // console.log('noble costs', concatenated(state_components).length);

    // // store current round
    // current round is not used at the moment, but would go here

    // store cost of each available noble
    for (let noble_index = 0; noble_index < state.num_nobles; noble_index++) {
        let noble = null;
        if (noble_index < state.nobles.length) {
            noble = state.nobles[noble_index];
        }
        for (let colour of colours) {
            arr = zeros(3);
            if (!(noble === null)) {
                let value = noble.cards[colour];
                if (value > 0) {
                    arr[value - 2] = 1;
                } else {
                    arr[0] = 1;
                }
            }
            state_components.push(arr);
        }
    }

    // console.log('card costs', concatenated(state_components).length);

    // store cost of each available card
    let tier = 1;
    let t1_max_gems = 5;
    for (let card_index = 0; card_index < 4; card_index++) {
        let card = null;
        if (card_index < state.cards_in_market[tier].length) {
            card = state.cards_in_market[tier][card_index];
        }
        for (let colour of colours) {
            arr = zeros(t1_max_gems);
            if (!(card === null)) {
                arr[card.gems[colour]] = 1;
            }
            state_components.push(arr);
        }
    }
    tier = 2;
    let t2_max_gems = 7;
    for (let card_index = 0; card_index < 4; card_index++) {
        let card = null;
        if (card_index < state.cards_in_market[tier].length) {
            card = state.cards_in_market[tier][card_index];
        }
        for (let colour of colours) {
            arr = zeros(t2_max_gems);
            if (!(card === null)) {
                arr[card.gems[colour]] = 1;
            }
            state_components.push(arr);
        }
    }
    tier = 3;
    let t3_max_gems = 8;
    for (let card_index = 0; card_index < 4; card_index++) {
        let card = null;
        if (card_index < state.cards_in_market[tier].length) {
            card = state.cards_in_market[tier][card_index];
        }
        for (let colour of colours) {
            arr = zeros(t3_max_gems);
            if (!(card === null)) {
                arr[card.gems[colour]] = 1;
            }
            state_components.push(arr);
        }
    }

    // console.log('player card costs', concatenated(state_components).length);

    // store cost of each card in player hands
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        for (let card_index = 0; card_index < 3; card_index++) {
            let card = null;
            if (card_index < player.cards_in_hand.length) {
                card = player.cards_in_hand[card_index];
            }
            for (let colour of colours) {
                arr = zeros(8);
                if (!(card === null)) {
                    arr[card.gems[colour]] = 1;
                }
                state_components.push(arr);
            }
        }
    }

    // console.log('card points', concatenated(state_components).length);

    // store points value of each available card
    let tier_num_diff_points = [2, 3, 3];
    let tier_min_points = [0, 1, 3];
    let tier_max_points = [1, 3, 5];
    for (let tier_index = 0; tier_index < 3; tier_index++) {
        let tier = tier_index + 1;
        for (let card_index = 0; card_index < 4; card_index++) {
            let card = null;
            arr = zeros(tier_num_diff_points[tier_index]);
            if (card_index < state.cards_in_market[tier].length) {
                card = state.cards_in_market[tier][card_index];
                arr[card.points - tier_min_points[tier_index]] = 1;
            }
            state_components.push(arr);
        }
    }

    // console.log('player card points', concatenated(state_components).length);

    // store points value of each card in player hands
    let hand_max_points = 6;
    let hand_num_diff_points = 6;
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        for (let card_index = 0; card_index < 3; card_index++) {
            let card = null;
            arr = zeros(hand_num_diff_points);
            if (card_index < player.cards_in_hand.length) {
                card = player.cards_in_hand[card_index];
                let points = card.points;
                arr[points] = 1;
            }
            state_components.push(arr);
        }
    }

    // console.log('num pointsless', concatenated(state_components).length);

    // store number of times a points-less card has been bought
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        arr = zeros(16);
        for (let i = 0; i < Math.min(player.num_no_points_buys(), 16); i++) {  
            arr[i] = 1;
        }
        // arr[Math.max(player.num_no_points_buys(), 15)] = 1;
        state_components.push(arr);
    }

    // console.log('num pointful', concatenated(state_components).length);

    // store number of times a pointful card has been bought
    for (let player_index of player_indices) {
        let player = state.players[player_index];
        arr = zeros(10);
        for (let i = 0; i < Math.min(player.num_points_buys(), 10); i++) {
            arr[i] = 1;
        }
        // arr[Math.min(player.num_points_buys(), 9)] = 1;
        state_components.push(arr);
    }
    
    // concatenate everything
    let output_arr = [];
    // console.log(state_components.length, 'state components');
    // for (let c of state_components) {
    //     console.log(c.length);
    // }
    for (let input_arr of state_components) {
        output_arr.push(...input_arr);
    }
    
    return output_arr;
}
