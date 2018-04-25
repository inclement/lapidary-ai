var colours = ['white', 'blue', 'green', 'red', 'black'];

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

        this.cards_in_hand.push(new Card(2, 'red', 7, {white: 2, green: 9}));
    }

    num_gems(colour) {
        return this.gems[colour];
    }

    can_afford(card) {
        return false;
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

        this.round_number = 1;

        shuffle(this.tier_1);
        shuffle(this.tier_2);
        shuffle(this.tier_3);
        
        this.refill_market();
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
