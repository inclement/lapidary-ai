var colours = ['white', 'blue', 'green', 'red', 'black'];
var all_colours = ['white', 'blue', 'green', 'red', 'black', 'gold'];

function sum(numbers) {
    var total = 0;
    for (var number of numbers) {
        total += number;
    }
    return total
}

class Player {
    constructor(number) {
        this.number = number;
        this.cards_in_hand = [];
        this.cards_played = [];
        this.nobles = [];

        this.gems = {white: 0,
                     blue: 0,
                     green: 0,
                     red: 0,
                     black: 0,
                     gold: 0};

        this.card_colours = {white: 0,
                             blue: 0,
                             green: 0,
                             red: 0,
                             black: 0};

        this.score = 0;

    }

    num_gems(colour) {
        return this.gems[colour];
    }

    add_gems(gems) {
        for (let colour of colours) {
            if (colour in gems) {
                this.gems[colour] += gems[colour];
            }
        }
    }

    can_afford(card) {

        var missing_colours = [];
        for (var colour of colours) {
            missing_colours.push(
                Math.max(card.gems[colour] -
                         this.gems[colour] -
                         this.card_colours[colour],
                         0));
        }

        if (sum(missing_colours) > this.gems['gold']) {
            return [false,
                    sum(missing_colours) - this.gems['gold']];
                    
        }

        var cost = {};
        for (let colour of colours) {
            cost[colour] = Math.max(
                Math.min(this.gems[colour],
                         card.gems[colour] - this.card_colours[colour]),
                0);
        }
        cost['gold'] = sum(missing_colours);

        return [true, cost];
    }
}

class GameState {
    constructor(num_players=2,
                init_game=false) {

        this.num_players = num_players;
        this.players = [];

        this.current_player_index = 0;

        this.num_gems_in_play = 4;  // should depend on num_players
        this.num_gold_gems_in_play = 5;
        this.num_dev_cards = 4;
        this.num_nobles = 2;  // should depend on num_players

        this.supply_gems = {white: this.num_gems_in_play,
                            blue: this.num_gems_in_play,
                            green: this.num_gems_in_play,
                            red: this.num_gems_in_play,
                            black: this.num_gems_in_play,
                            gold: this.num_gold_gems_in_play};

        for (var i = 0; i < this.num_players; i++) {
            this.players.push(new Player(i + 1));
        }

        this.tier_1 = tier_1.slice();
        this.tier_1_visible = [];
        this.tier_2 = tier_2.slice();
        this.tier_2_visible = [];
        this.tier_3 = tier_3.slice();
        this.tier_3_visible = [];

        this.cards_in_deck = {1: this.tier_1,
                              2: this.tier_2,
                              3: this.tier_3}

        this.cards_in_market = {1: this.tier_1_visible,
                                2: this.tier_2_visible,
                                3: this.tier_3_visible}

        this.round_number = 1;

        shuffle(this.tier_1);
        shuffle(this.tier_2);
        shuffle(this.tier_3);
        
        this.refill_market();

        this.moves = [];
    }

    refill_market() {
        while (this.tier_1_visible.length < 4 &&
               this.tier_1.length > 0) {
            var card = this.tier_1.pop();
            this.tier_1_visible.push(card);
        }

        while (this.tier_2_visible.length < 4 &&
               this.tier_2.length > 0) {
            var card = this.tier_2.pop();
            this.tier_2_visible.push(card);
        }

        while (this.tier_3_visible.length < 4 &&
               this.tier_3.length > 0) {
            var card = this.tier_3.pop();
            this.tier_3_visible.push(card);
        }
    }

    make_move(move) {
        this.moves.push(move);

        var player = this.players[this.current_player_index];
        
        if (move['action'] === 'gems') {
            player.add_gems(move['gems']);
            var gems = move['gems'];
            for (let colour of colours) {
                if (colour in gems) {
                    this.supply_gems[colour] -= gems[colour];
                }
            }
        } else if (move['action'] === 'buy_available') {
            let tier = move['tier'];
            let index = move['index'];
            let gems = move['gems'];
            let numeric_tier = parseInt(tier);

            var card = this.cards_in_market[numeric_tier][index];
            this.cards_in_market[numeric_tier].splice(index, 1);

            console.log('card is', card);
            player.cards_played.push(card);
            player.card_colours[card.colour] += 1;
            console.log(card.colour);

            for (let colour of all_colours) {
                if (colour in gems) {
                    player.gems[colour] -= gems[colour];
                    this.supply_gems[colour] += gems[colour];
                }
            }

        } else if (move['action'] === 'buy_reserved') {
            let index = move['index'];
            let gems = move['gems'];

            var card = player.cards_in_hand[index];
            player.cards_in_hand.splice(index, 1);

            player.cards_played.push(card);
            player.card_colours[card.colour] += 1;

            for (let colour of all_colours) {
                if (colour in gems) {
                    player.gems[colour] -= gems[colour];
                    this.supply_gems[colour] += gems[colour];
                }
            }
        } else if (move['action'] === 'reserve') {
            var card;
            if (move['index'] == -1) {
                card = this.cards_in_deck[move['tier']].pop();
            } else {
                card = this.cards_in_market[move['tier']][move['index']];
                this.cards_in_market[move['tier']].splice(move['index'], 1);
            }

            player.cards_in_hand.push(card);

            var gems = move['gems'];
            if ('gold' in gems) {  // no other colour can appear
                player.gems['gold'] += gems['gold'];
                this.supply_gems['gold'] -= 1;
            }

        }

        // Assign nobles if necessary
        // TODO

        // Clean up the state
        this.refill_market();
        // TODO: Update the state vector here

        // TODO: Validate here

        this.current_player_index += 1;
        this.current_player_index %= this.num_players;
        if (this.current_player_index == 0) {
            this.round_number += 1;
        }
        
        return this;
    }

    reduce_gems() {
        this.supply_gems['green'] -= 2;
        this.supply_gems['blue'] += 1;
        this.players[0].score += 1;

        this.players[0].gems['red'] += 5;

        this.tier_1_visible.pop();
        this.refill_market();

        this.round_number += 1;
    }
}

class Card {
    constructor(tier, colour, points,
                gems) {
        // {white:0, blue:0, green:0, red:0, black:0}) {
        this.tier = tier;
        this.colour = colour;
        this.points = points;

        this.gems = gems;
        for (var colour of colours) {
            if (!gems.hasOwnProperty(colour)) {
                gems[colour] = 0;
            }
        }
    }
}

var tier_1 = [
    new Card(1, 'blue', 0, {black:3}),
    new Card(1, 'blue', 0, {white:1, black:2}),
    new Card(1, 'blue', 0, {green:2, black:2}),
    new Card(1, 'blue', 0, {white:1, green:2, red:2}),
    new Card(1, 'blue', 0, {blue:1, green:3, red:1}),
    new Card(1, 'blue', 0, {white:1, green:1, red:1, black:1}),
    new Card(1, 'blue', 0, {white:1, green:1, red:2, black:1}),
    new Card(1, 'blue', 1, {red:4}),

    new Card(1, 'red', 0, {white:3}),
    new Card(1, 'red', 0, {blue:2, green:1}),
    new Card(1, 'red', 0, {white:2, red:2}),
    new Card(1, 'red', 0, {white:2, green:1, black:2}),
    new Card(1, 'red', 0, {white:1, red:1, black:3}),
    new Card(1, 'red', 0, {white:1, blue:1, green:1, black:1}),
    new Card(1, 'red', 0, {white:2, blue:1, green:1, black:1}),
    new Card(1, 'red', 1, {white:4}),

    new Card(1, 'black', 0, {green:3}),
    new Card(1, 'black', 0, {green:2, red:1}),
    new Card(1, 'black', 0, {white:2, green:2}),
    new Card(1, 'black', 0, {white:2, blue:2, red:1}),
    new Card(1, 'black', 0, {green:1, red:3, black:1}),
    new Card(1, 'black', 0, {white:1, blue:1, green:1, red:1}),
    new Card(1, 'black', 0, {white:1, blue:2, green:1, red:1}),
    new Card(1, 'black', 1, {blue:4}),

    new Card(1, 'white', 0, {blue:3}),
    new Card(1, 'white', 0, {red:2, black:1}),
    new Card(1, 'white', 0, {blue:2, black:2}),
    new Card(1, 'white', 0, {blue:2, green:2, black:1}),
    new Card(1, 'white', 0, {white:3, blue:1, black:1}),
    new Card(1, 'white', 0, {blue:1, green:1, red:1, black:1}),
    new Card(1, 'white', 0, {blue:1, green:2, red:1, black:1}),
    new Card(1, 'white', 1, {green:4}),

    new Card(1, 'green', 0, {red:3}),
    new Card(1, 'green', 0, {white:2, blue:1}),
    new Card(1, 'green', 0, {blue:2, red:2}),
    new Card(1, 'green', 0, {blue:1, red:2, black:2}),
    new Card(1, 'green', 0, {white:1, blue:3, green:1}),
    new Card(1, 'green', 0, {white:1, blue:1, red:1, black:1}),
    new Card(1, 'green', 0, {white:1, blue:1, red:1, black:2}),
    new Card(1, 'green', 1, {black:4})
];

var tier_2 = [
    new Card(2, 'blue', 1, {blue:2, green:2, red:3}),
    new Card(2, 'blue', 1, {blue:2, green:3, black:3}),
    new Card(2, 'blue', 2, {blue:5}),
    new Card(2, 'blue', 2, {white:5, blue:3}),
    new Card(2, 'blue', 2, {white:2, red:1, black:4}),
    new Card(2, 'blue', 3, {blue:6}),

    new Card(2, 'red', 1, {white:2, red:2, black:3}),
    new Card(2, 'red', 1, {blue:3, red:2, black:3}),
    new Card(2, 'red', 2, {black:5}),
    new Card(2, 'red', 2, {white:3, black:5}),
    new Card(2, 'red', 2, {white:1, blue:4, green:2}),
    new Card(2, 'red', 3, {red:6}),

    new Card(2, 'black', 1, {white:3, blue:2, green:2}),
    new Card(2, 'black', 1, {white:3, green:3, black:2}),
    new Card(2, 'black', 2, {white:5}),
    new Card(2, 'black', 2, {green:5, red:3}),
    new Card(2, 'black', 2, {blue:1, green:4, red:2}),
    new Card(2, 'black', 3, {black:6}),

    new Card(2, 'white', 1, {green:3, red:2, black:2}),
    new Card(2, 'white', 1, {white:2, blue:3, red:3}),
    new Card(2, 'white', 2, {red:5}),
    new Card(2, 'white', 2, {red:5, black:3}),
    new Card(2, 'white', 2, {green:1, red:4, black:2}),
    new Card(2, 'white', 3, {white:6}),

    new Card(2, 'green', 1, {white:2, blue:3, black:2}),
    new Card(2, 'green', 1, {white:3, green:2, red:3}),
    new Card(2, 'green', 2, {green:5}),
    new Card(2, 'green', 2, {blue:5, green:3}),
    new Card(2, 'green', 2, {white:4, blue:2, black:1}),
    new Card(2, 'green', 3, {green:6})
];

var tier_3 = [
    new Card(3, 'blue', 3, {white:3, green:3, red:3, black:5}),
    new Card(3, 'blue', 4, {white:7}),
    new Card(3, 'blue', 4, {white:6, blue:3, black:3}),
    new Card(3, 'blue', 5, {white:7, blue:3}),

    new Card(3, 'red', 3, {white:3, blue:5, green:3, black:5}),
    new Card(3, 'red', 4, {green:7}),
    new Card(3, 'red', 4, {blue:3, green:6, red:3}),
    new Card(3, 'red', 5, {green:7, red:3}),

    new Card(3, 'black', 3, {white:3, blue:3, green:5, red:3}),
    new Card(3, 'black', 4, {red:7}),
    new Card(3, 'black', 4, {green:3, red:6, black:3}),
    new Card(3, 'black', 5, {red:7, black:3}),

    new Card(3, 'white', 3, {blue:3, green:3, red:5, black:3}),
    new Card(3, 'white', 4, {black:7}),
    new Card(3, 'white', 4, {white:3, red:3, black:6}),
    new Card(3, 'white', 5, {white:3, black:7}),

    new Card(3, 'green', 3, {white:5, blue:3, red:3, black:3}),
    new Card(3, 'green', 4, {blue:7}),
    new Card(3, 'green', 4, {white:3, blue:6, green:3}),
    new Card(3, 'green', 5, {blue:7, green:3})
];
