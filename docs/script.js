var background_colours = {
    'white': '#ffffff',
    'blue': '#bbbbff',
    'red': '#ffbbbb',
    'green': '#bbffbb',
    'black': '#aaaaaa',
    'gold': '#ffffbb'
};

var border_colours = {
    'white': 'lightgrey',
    'blue': 'blue',
    'red': 'red',
    'green': 'green',
    'black': 'black',
    'gold': 'gold'
};

var a = math.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]);
var b = math.matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]]);

// shuffle function from https://bost.ocks.org/mike/algorithms/#shuffling
function shuffle(array) {
    var n = array.length,
        t,
        i;
    while (n) {
        i = Math.random() * n-- | 0; // 0 ≤ i < n
        t = array[n];
        array[n] = array[i];
        array[i] = t;
    }
    return array;
}

var test_state = new GameState();

Vue.component('gems-table', {
    props: ['gems', 'cards', 'show_card_count'],
    template: '\n<table class="gems-table">\n  <tr>\n    <gems-table-gem-counter v-for="(number, colour) in gems"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-gem-counter>\n  </tr>\n  <tr v-if="show_card_count">\n    <gems-table-card-counter v-for="(number, colour) in cards"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-card-counter>\n  </tr>\n</table>\n'
});

Vue.component('gems-table-gem-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function () {
            return border_colours[this.colour];
        },
        background_colour: function () {
            return background_colours[this.colour];
        }
    },
    template: '\n<td class="gems-table-gem-counter"\n    v-bind:style="{background: background_colour, borderColor: border_colour}">\n  {{ number }}\n</td>\n'
});

Vue.component('gems-table-card-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function () {
            return border_colours[this.colour];
        },
        background_colour: function () {
            return background_colours[this.colour];
        }
    },
    template: '\n<td class="gems-table-card-counter"\n    v-bind:style="{background: background_colour, borderColor: border_colour}">\n  {{ number }}\n</td>\n'
});

Vue.component('gems-list', {
    props: { gems: {},
        title: "",
        display_zeros: { default: true } },
    template: '\n<div class="gems-list">\n    <h3 v-if="title">{{ title }}</h3>\n    <ul>\n    <gem-counter \n        v-for="(number, colour) in gems"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number"\n        style="font-size:2vh;"\n        v-if="number > 0 || display_zeros">\n    </gem-counter>\n    </ul>\n</div>'
});

Vue.component('gem-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function () {
            return border_colours[this.colour];
        },
        background_colour: function () {
            return background_colours[this.colour];
        }
    },
    template: '\n<li class="gem-counter" \n    v-bind:style="{background: background_colour, borderColor: border_colour}">\n  {{ number }}\n</li>\n'
});

Vue.component('gem-discarder', {
    props: ['player', 'gems_discarded', 'player_gems'],
    methods: {
        discard_gems: function () {
            this.$emit('discard_gems');
        }
    },
    template: '\n<div class="gem-discarder">\n  <h3>discard gems</h3>\n  <gem-discarder-table v-bind:gems_discarded="gems_discarded"\n                       v-bind:player_gems="player.gems">\n  </gem-discarder-table>\n  <button v-on:click="discard_gems()">\n    confirm discards\n  </button>\n</div>\n'
});

Vue.component('gem-discarder-table', {
    props: ['player_gems', 'gems_discarded'],
    methods: {
        increment(colour) {
            this.player_gems[colour] += 1;
            this.gems_discarded[colour] -= 1;
        },
        decrement(colour) {
            this.player_gems[colour] -= 1;
            this.gems_discarded[colour] += 1;
        }
    },
    computed: {
        total_player_gems: function () {
            let total_gems = 0;
            for (let colour of all_colours) {
                total_gems += this.player_gems[colour];
            }
            return total_gems;
        },
        can_increment: function () {
            let incrementable = {};
            for (let colour of all_colours) {
                incrementable[colour] = this.gems_discarded[colour] > 0;
            }
            return incrementable;
        },
        can_decrement: function () {
            let decrementable = {};
            let total_gems = this.total_player_gems;
            for (let colour of all_colours) {
                decrementable[colour] = total_gems > 10 && this.player_gems[colour] > 0;
            }
            return decrementable;
        }
    },
    template: '\n<table class="gem-discarder-table">\n  <tr>\n    <td>\n        current gems\n    </td>\n    <gems-table-gem-counter v-for="(number, colour) in player_gems"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-gem-counter>\n  </tr>\n  <tr>\n    <td>\n    </td>\n    <increment-button v-for="(number, colour) in player_gems"\n                      v-bind:key="colour"\n                      v-bind:enabled="can_increment[colour]"\n                      v-on:increment="increment($event)"\n                      v-bind:colour="colour">\n e  </increment-button>\n  </tr>\n  <tr>\n    <td>\n    </td>\n    <decrement-button v-for="(number, colour) in player_gems"\n                      v-bind:key="colour"\n                      v-bind:enabled="can_decrement[colour]"\n                      v-on:decrement="decrement($event)"\n                      v-bind:colour="colour">\n    </decrement-button>\n  </tr>\n  <tr>\n    <td>\n        discarded gems\n    </td>\n    <gems-table-gem-counter v-for="(number, colour) in gems_discarded"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-gem-counter>\n  </tr>\n</table>\n'
});

Vue.component('move-maker', {
    props: ['player', 'supply_gems', 'gems', 'player_gems', 'player_cards'],
    methods: {
        take_gems: function () {
            this.$emit('take_gems', this.gems);
        }
    },
    computed: {
        any_gems_selected: function () {
            var any_gems_in_supply = false;
            for (let colour of colours) {
                if (this.supply_gems[colour] > 0) {
                    any_gems_in_supply = true;
                    break;
                }
            }

            if (!any_gems_in_supply) {
                return true; // no gems in supply, so can 'take gems'
                // without selecting any
            }

            var any_selected = false;
            for (let colour of colours) {
                if (this.gems[colour] > 0) {
                    any_selected = true;
                    break;
                }
            }
            return any_selected;
        }
    },
    template: '\n<div class="move-maker">\n  <gem-selector v-bind:supply_gems="supply_gems"\n                v-bind:player_gems="player_gems"\n                v-bind:player_cards="player_cards"\n                v-bind:gems="gems">\n  </gem-selector>\n  <button v-on:click="take_gems()"\n          v-bind:disabled="!any_gems_selected && false">\n    take gems\n  </button>\n</div>\n'
});

Vue.component('gem-selector', {
    props: ['supply_gems', 'gems', 'player_gems', 'player_cards'],
    computed: {
        can_increment: function () {
            var any_value_2 = false;
            var num_values_1 = 0;
            for (var i = 0; i < colours.length; i++) {
                var colour = colours[i];
                if (this.gems[colour] >= 2) {
                    any_value_2 = true;
                }
                if (this.gems[colour] == 1) {
                    num_values_1 += 1;
                }
            }
            var incrementable = {};
            for (var i = 0; i < colours.length; i++) {
                var colour = colours[i];
                incrementable[colour] = !any_value_2 && (num_values_1 == 1 && this.gems[colour] == 1 && this.supply_gems[colour] > 3 || num_values_1 < 3 && this.supply_gems[colour] > 0 && this.gems[colour] == 0);
            }
            return incrementable;
        },
        can_decrement: function () {
            var decrementable = {};
            for (var i = 0; i < colours.length; i++) {
                var colour = colours[i];
                decrementable[colour] = this.gems[colour] > 0;
            }
            return decrementable;
        },
        show_button: function () {
            let show = {};
            for (let colour of colours) {
                if (this.supply_gems[colour] > 0) {
                    show[colour] = true;
                } else {
                    show[colour] = false;
                }
            }
            show['gold'] = false;
            return show;
        }
    },
    template: '\n<table class="gem-selector">\n  <tr style="margin-bottom:15px">\n    <td>current gems</td>\n    <gems-table-gem-counter v-for="(number, colour) in player_gems"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-gem-counter>\n  </tr>\n  <tr style="margin-bottom:15px">\n    <td>current cards</td>\n    <gems-table-card-counter v-for="(number, colour) in player_cards"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-card-counter>\n  </tr>\n  <tr><td style="height:7px"></td></tr>\n  <tr>\n    <td>gems gained</td>\n    <gems-table-gem-counter v-for="(number, colour) in gems"\n        v-bind:key="colour"\n        v-bind:colour="colour"\n        v-bind:number="number">\n    </gems-table-gem-counter>\n  </tr>\n  <tr>\n    <td></td>\n    <increment-button v-for="(number, colour) in gems"\n                      v-bind:key="colour"\n                      v-bind:enabled="can_increment[colour]"\n                      v-bind:show_button="show_button[colour]"\n                      v-on:increment="gems[$event] += 1"\n                      v-bind:colour="colour">\n    </increment-button>\n  </tr>\n  <tr>\n    <td></td>\n    <decrement-button v-for="(number, colour) in gems"\n                      v-bind:key="colour"\n                      v-bind:enabled="can_decrement[colour]"\n                      v-bind:show_button="show_button[colour]"\n                      v-on:decrement="gems[$event] -= 1"\n                      v-bind:colour="colour">\n    </decrement-button>\n  </tr>\n</table>\n'
});

Vue.component('increment-button', {
    props: ['colour', 'enabled', 'show_button'],
    computed: {
        show: function () {
            if (this.show_button) {
                return 1;
            }
            return 0;
        }
    },
    template: '\n<td class="increment-button">\n  <button v-bind:disabled="!enabled"\n          v-bind:style="{opacity:show}"\n          v-on:click="$emit(\'increment\', colour)">\n    +\n  </button>\n</td>\n'
});

Vue.component('decrement-button', {
    props: ['colour', 'enabled', 'show_button'],
    computed: {
        show: function () {
            if (this.show_button) {
                return 1;
            }
            return 0;
        }
    },
    template: '\n<td class="decrement-button">\n  <button v-bind:disabled="!enabled"\n          v-bind:style="{opacity:show}"\n          v-on:click="$emit(\'decrement\', colour)">\n    -\n  </button>\n</td>\n'
});

Vue.component('player-display', {
    props: ['player', 'is_current_player', 'show_card_buttons', 'is_human'],
    computed: {
        player_num_gems: function () {
            return this.player.gems['white'] + this.player.gems['blue'] + this.player.gems['green'] + this.player.gems['red'] + this.player.gems['black'] + this.player.gems['gold'];
        },
        border_width: function () {
            if (this.is_current_player) {
                return "6px";
            }
            return "5px";
        },
        border_colour: function () {
            if (this.is_current_player) {
                return 'green';
            }
            return '#bbeebb';
        },
        background_colour: function () {
            if (this.is_current_player) {
                return '#eeffee';
            }
            return '#ffffee';
        },
        player_type: function () {
            if (this.is_human) {
                return 'you';
            }
            return 'AI';
        }
    },
    template: '\n<div class="player-display"\n     v-bind:style="{borderWidth: border_width,borderColor: border_colour,backgroundColor: background_colour}">\n<h3>P{{ player.number }} ({{ player_type }}): {{ player.score }} points, {{ player_num_gems }} gems</h3>\n    <gems-table v-bind:gems="player.gems"\n                v-bind:show_card_count="true"\n                v-bind:cards="player.card_colours">\n    </gems-table>\n    <cards-display v-show="player.cards_in_hand.length > 0"\n                   v-bind:cards="player.cards_in_hand"\n                   v-bind:player="player"\n                   v-bind:num_cards="3"\n                   tier="hand"\n                   v-bind:show_card_buttons="show_card_buttons"\n                   v-bind:show_reserve_button="false"\n                   style="height:180px;min-height:180px"\n                   v-on:buy="$emit(\'buy\', $event)">\n    </cards-display>\n    <nobles-display v-bind:nobles="player.nobles">\n    </nobles-display>\n</div>\n'
});

Vue.component('cards-display', {
    props: ['cards', 'name', 'tier', 'player', 'show_reserve_button', 'num_cards', 'show_card_buttons'],
    methods: {
        reserve: function (card) {
            var card_index;
            for (var i = 0; i < this.cards.length; i++) {
                if (this.cards[i] === card) {
                    card_index = i;
                }
            }
            this.$emit('reserve', [this.tier, card_index]);
        },
        buy: function (card) {
            var card_index;
            for (var i = 0; i < this.cards.length; i++) {
                if (this.cards[i] === card) {
                    card_index = i;
                }
            }
            this.$emit('buy', [this.tier, card_index, this.player.can_afford(card)[1]]);
        }
    },
    computed: {
        card_width: function () {
            return ((100 - this.num_cards * 2) / this.num_cards).toString() + '%';
        }
    },
    template: '\n<div class="cards-display">\n    <h3>{{ name }}</h3>\n    <ul class="single-line-list">\n      <card-display\n          v-bind:style="{width:card_width,maxWidth:card_width,minWidth:card_width}"\n          v-for="card in cards"\n          v-bind:show_reserve_button="show_reserve_button"\n          v-bind:show_card_buttons="show_card_buttons"\n          v-bind:player="player"\n          v-bind:key="card.id"\n          v-bind:card="card" \n          v-on:buy="buy($event)"\n          v-on:reserve="reserve($event)">\n      </card-display>\n    </ul>\n</div>\n'
});

Vue.component('card-display', {
    props: ['card', 'player', 'show_reserve_button', 'show_card_buttons'],
    computed: {
        background_colour: function () {
            return background_colours[this.card.colour];
        },
        buyable: function () {
            return this.player.can_afford(this.card)[0];
        },
        reservable: function () {
            return this.player.cards_in_hand.length < 3;
        },
        buy_button_top: function () {
            if (this.show_reserve_button) {
                return "26%";
            }
            return "5%";
        }
    },
    template: '\n<li class="card-display">\n<div class="card-display-contents" v-bind:style="{backgroundColor: background_colour}">\n    <p class="card-points">{{ card.points }}</p>\n    <button class="reserve-button"\n            v-if="show_reserve_button && show_card_buttons && reservable"\n            v-bind:disabled="!reservable"\n            v-on:click="$emit(\'reserve\', card)">\n        reserve\n    </button>\n    <button class="buy-button"\n            v-if="show_card_buttons && buyable"\n            v-bind:disabled="!buyable"\n            v-bind:style="{top: buy_button_top}"\n            v-on:click="$emit(\'buy\', card)">\n        buy\n    </button>\n    <gems-list v-bind:gems="card.gems" \n               v-bind:display_zeros="false">\n    </gems-list>\n</div>\n</li>\n'
});

Vue.component('card-display-table-row', {
    props: ['colour', 'number', 'other'],
    template: '\n<tr>\n  <td>\n    <gem-counter v-bind:colour="colour"\n                 v-bind:number="number">\n    </gem-counter>\n  </td>\n</tr>\n'
});

Vue.component('supply-display', {
    props: ['gems', 'show_card_count', 'nobles'],
    computed: {
        num_gems: function () {
            let total = 0;
            for (let colour of colours) {
                total += this.gems[colour];
            }
            return total;
        }
    },
    template: '\n<div class="supply-display">\n    <h3>Supply: {{ num_gems }} coloured gems</h3>\n    <gems-table v-bind:gems="gems"\n                v-bind:show_card_count="show_card_count">\n    </gems-table>\n    <nobles-display v-bind:nobles="nobles">\n    </nobles-display>\n</div>\n'
});

function noble_string(noble) {
    let string = '<span class="bold">3 points</span> for ';
    let first = true;
    for (let colour of colours) {
        if (colour in noble.cards && noble.cards[colour] > 0) {
            if (!first) {
                string += ', ';
            }
            string += '<span class="' + colour + '">' + noble.cards[colour] + ' ' + colour + '</span>';
            first = false;
        }
    }
    return string;
};

Vue.component('nobles-display', {
    props: ['nobles'],
    computed: {
        noble_strings: function () {
            let strings = [];
            for (let noble of this.nobles) {
                strings.push(noble_string(noble));
            }
            return strings;
        }
    },
    template: '\n<ul class="nobles-display">\n    <li v-for="noble_string in noble_strings"><span v-html="noble_string"></span></li>\n</ul>\n'
});

Vue.component('ai-move-status', {
    props: ['player_index', 'num_possible_moves'],
    watch: {
        player_index: function (val) {
            this.$emit('on_player_index');
        }
    },
    template: '\n<div class="ai-move-status">\n    <h3>Player {{ player_index + 1 }} (AI) thinking: {{ num_possible_moves }} possible moves.</h3>\n    <div class="loader-positioner">\n        <div class="loader"></div>\n    </div>\n</div>\n'
});

Vue.component('winner-display', {
    props: ['winner_index', 'players'],
    computed: {
        winning_score: function () {
            if (this.winner_index === null) {
                return -1;
            }
            return this.players[this.winner_index].score;
        }
    },
    template: '\n<div class="winner-display">\n    <h3>Player {{ winner_index + 1 }} wins with {{ winning_score }} points!\n    </h3>\n\n    <button v-on:click="$emit(\'reset\')">\n        play again\n    </button>\n</div>\n'
});

function move_to_html(move) {
    let action = move['action'];
    let html = '';
    if (action === 'gems') {
        html += 'took gems: ';
        let gems = move['gems'];
        for (let colour of all_colours) {
            if (colour in gems && gems[colour] != 0) {
                let number = gems[colour];
                html += '<span class="' + colour + '">' + number + '</span>&nbsp;';
            }
        }
    } else if (action === 'reserve') {
        let card = move['card'];
        html += 'reserved ' + card.points + ' point <span class="' + card.colour + '">' + card.colour + '</span> card costing ';
        for (let colour of colours) {
            if (colour in card.gems && card.gems[colour] != 0) {
                let number = card.gems[colour];
                html += '<span class="' + colour + '">' + number + '</span>&nbsp;';
            }
        }
        html += 'from tier ' + move['tier'];
        if (move['gems']['gold'] != 0) {
            html += ', gaining <span class="gold">' + move['gems']['gold'] + '</span>';
        }
        //     + ' paying ';
        // let gems = move['gems'];
        // for (let colour of all_colours) {
        //     if (colour in gems && gems[colour] != 0) {
        //         let number = gems[colour];
        //         html += '<span class="' + colour +'">' + number + '</span> ';
        //     }
        // }
    } else if (action === 'buy_reserved' || action === 'buy_available') {
        let card = move['card'];
        html += 'bought ' + card.points + ' point <span class="' + card.colour + '">' + card.colour + '</span> card costing ';
        for (let colour of colours) {
            if (colour in card.gems && card.gems[colour] != 0) {
                let number = card.gems[colour];
                html += '<span class="' + colour + '">' + number + '</span>&nbsp;';
            }
        }
        if (action === 'buy_reserved') {
            html += 'from hand for ';
        } else {
            html += 'from tier ' + move['tier'] + ' for ';
        }
        let cost = move['gems'];
        let was_free = true;
        for (let colour of all_colours) {
            if (colour in cost && cost[colour] != 0) {
                let number = cost[colour];
                was_free = false;
                html += '<span class="' + colour + '">' + number + '</span>&nbsp;';
            }
        }
        if (was_free) {
            html += 'free';
        }
    }
    return html;
}

Vue.component('moves-log-display', {
    props: ['moves'],
    computed: {
        move_strings: function () {
            let strs = [];
            for (let i = 0; i < this.moves.length; i++) {
                let move = this.moves[i];
                let round = math.floor(i / 2) + 1;
                let player = i % 2 + 1;

                let html = move_to_html(move);
                strs.push('<span class="bold">R' + round + ' P' + player + ':</span> ' + html);
            }
            return strs;
        }
    },
    template: '\n<div class="moves-log-display"\n     v-if="moves.length > 0">\n    <h3>Moves log:</h3>\n    <ul>\n        <li v-for="move in move_strings"><span v-html="move"></span></li>\n    </ul>\n</div>\n'
});

function random_player_index() {
    if (math.random() > 0.5) {
        return 1;
    }
    return 0;
}

var app = new Vue({
    el: '#app',
    data: {
        state: test_state,
        human_player_indices: [random_player_index()],
        scheduled_move_func: null,
        discarding: false,
        winner_index: null,
        num_possible_moves: 0,
        debug_checked: false,
        gems_selected: { 'white': 0,
            'blue': 0,
            'green': 0,
            'red': 0,
            'black': 0,
            'gold': 0 },
        gems_discarded: { 'white': 0,
            'blue': 0,
            'green': 0,
            'red': 0,
            'black': 0,
            'gold': 0 }
    },
    methods: {
        testChangeGems: function () {
            this.state.reduce_gems();
        },
        test_state_vector: function () {
            // for (let i = 0; i < 100; i++) {
            //     this.state.get_state_vector(0);
            // }
            console.log(this.state.get_state_vector());
            console.log('state vector length is', this.state.get_state_vector().length);
        },
        test_ai_move: function () {
            console.log('ai move:', ai.make_move(this.state));
        },
        test_change_player_type: function () {
            if (this.player_type === 'human') {
                this.player_type = 'ai';
            } else {
                this.player_type = 'human';
            }

            for (var i = 0; i < colours.length; i++) {
                this.gems_selected[colours[i]] = 0;
            }
        },
        test_moves: function () {
            console.log(this.state.get_valid_moves());
        },
        random_move: function () {
            let ai = new RandomAI();
            let move = ai.make_move(this.state);
            this.state.make_move(move);
        },
        test_win: function () {
            this.state.players[0].score = 15;
        },
        reset: function () {
            this.human_player_indices = [random_player_index()];
            this.state = new GameState();
            // this.player_type = 'human';
            this.discarding = false;
            this.winner_index = null;

            for (let colour of all_colours) {
                this.gems_selected[colour] = 0;
            }
            if (this.player_type === 'ai') {
                this.schedule_ai_move();
            }
        },
        on_player_index: function () {
            let winner = this.state.has_winner();
            if (this.state.current_player_index === 0 && !(winner === null)) {
                this.winner_index = winner;
                return;
            }

            if (!(this.scheduled_move_func === null)) {
                window.clearTimeout(this.scheduled_move_func);
                this.scheduled_move_func = null;
            }
            if (this.player_type === 'ai') {
                this.schedule_ai_move();
            }
        },
        schedule_ai_move: function () {
            this.num_possible_moves = this.state.get_valid_moves(this.state.current_player_index).length;
            window.setTimeout(this.do_ai_move, 600);
        },
        nn_ai_move: function () {
            console.log('Doing nn ai move');
            let move = ai.make_move(this.state);
            console.log('ai move is', move);
            this.state.make_move(move);
        },
        do_ai_move: function () {
            this.scheduled_move_func = null;
            // this.random_move();
            if (this.player_type === 'ai') {
                this.nn_ai_move();
            }
        },
        do_move_gems: function (info) {
            let passed_gems = {};
            for (let colour of all_colours) {
                if (colour in this.gems_selected) {
                    passed_gems[colour] = this.gems_selected[colour];
                }
            }
            this.state.make_move({ action: 'gems',
                gems: passed_gems }, false);
            for (let colour of colours) {
                this.gems_selected[colour] = 0;
            }

            this.check_if_discarding();
        },
        do_move_reserve: function (info) {
            var gold_taken = 0;
            if (this.state.supply_gems['gold'] > 0) {
                gold_taken = 1;
            }
            this.state.make_move({ action: 'reserve',
                tier: info[0],
                index: info[1],
                gems: { 'gold': gold_taken } }, false);
            this.check_if_discarding();
        },
        do_move_buy: function (info) {
            let tier = info[0];
            if (tier === 'hand') {
                this.state.make_move({ action: 'buy_reserved',
                    tier: info[0],
                    index: info[1],
                    gems: info[2] }, false);
            } else {
                this.state.make_move({ action: 'buy_available',
                    tier: info[0],
                    index: info[1],
                    gems: info[2] }, false);
            }
            this.check_if_discarding();
        },
        check_if_discarding() {
            // let player = this.human_player;
            let player = this.current_player;
            if (player.total_num_gems() > 10) {
                this.discarding = true;
            } else {
                this.discarding = false;
                this.state.increment_player();
            }
        },
        do_discard_gems: function () {
            let player = this.current_player;
            let state = this.state;
            for (let colour of all_colours) {
                // player.gems[colour] -= this.gems_discarded[colour];
                state.supply_gems[colour] += this.gems_discarded[colour];
                this.gems_discarded[colour] = 0;
            }
            this.check_if_discarding();
        }
    },
    computed: {
        player_type: function () {
            // return 'human';
            for (let index of this.human_player_indices) {
                if (index === this.state.current_player_index) {
                    return 'human';
                }
            }
            return 'ai';
        },
        current_player: function () {
            return this.state.players[this.state.current_player_index];
        },
        human_player: function () {
            return this.state.players[this.human_player_index];
        },
        round_number: function () {
            return this.state.round_number;
        },
        supply_gems: function () {
            return this.state.supply_gems;
        },
        players: function () {
            return this.state.players;
        },
        indexed_players: function () {
            var players = {};
            for (let i = 0; i < this.num_players; i++) {
                players[i] = this.players[i];
            }
            return players;
        },
        show_card_buttons: function () {
            return !this.discarding && this.player_type === 'human' && this.winner_index === null;
        },
        has_winner: function () {
            return !(this.winner_index === null);
        }
    }
});

if (app.human_player_indices[0] != 0) {
    app.schedule_ai_move();
}