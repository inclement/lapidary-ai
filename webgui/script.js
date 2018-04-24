var background_colours = {
    'white': '#ffffff',
    'blue': '#bbbbff',
    'red': '#ffbbbb',
    'green': '#bbffbb',
    'black': '#aaaaaa',
    'gold': '#ffffbb',
};

var border_colours = {
    'white': 'lightgrey',
    'blue': 'blue',
    'red': 'red',
    'green': 'green',
    'black': 'black',
    'gold': 'gold',
};

var colours = ['white', 'blue', 'green', 'red', 'black'];

// shuffle function from https://bost.ocks.org/mike/algorithms/#shuffling
function shuffle(array) {
    var n = array.length, t, i;
    while (n) {
        i = Math.random() * n-- | 0; // 0 ≤ i < n
        t = array[n];
        array[n] = array[i];
        array[i] = t;
    }
    return array;
}

class GemsList {
    constructor(gems) {
        if (gems instanceof GemsList) {
            gems = gems.gems;
        }
        this.gems = gems;

        for (var i = 0, size = colours.length; i < size; i++) {
            var colour = colours[i];
            if (!(colour in this.gems)) {
                this.gems[colour] = 0;
            }
        }
    }

    add(gemslist) {
        for (var i = 0, size = colours.length; i < size; i++) {
            var colour = colours[i];
            this.gems[colour] += gemslist.gems[colour];
        }
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
        // this.gems = {
        //     white: white,
        //     blue: blue,
        //     green: green,
        //     red: red,
        //     black: black
        // };
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

var test_state = new GameState();


Vue.component('gems-table', {
    props: ['gems', 'cards', 'show_card_count'],
    template: `
<table class="gems-table">
  <tr>
    <gems-table-gem-counter v-for="(number, colour) in gems"
        v-bind:key="colour"
        v-bind:colour="colour"
        v-bind:number="number">
    </gems-table-gem-counter>
  </tr>
  <tr v-if="show_card_count">
    <gems-table-card-counter v-for="(number, colour) in gems"
        v-bind:key="colour"
        v-bind:colour="colour"
        v-bind:number="number">
    </gems-table-card-counter>
  </tr>
</table>
`
});

Vue.component('gems-table-gem-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function() {
            return border_colours[this.colour];
        },
        background_colour: function() {
            return background_colours[this.colour];
        }
    },
    template: `
<td class="gems-table-gem-counter"
    v-bind:style="{background: background_colour, borderColor: border_colour}">
  {{ number }}
</td>
`
});

Vue.component('gems-table-card-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function() {
            return border_colours[this.colour];
        },
        background_colour: function() {
            return background_colours[this.colour];
        }
    },
    template: `
<td class="gems-table-card-counter"
    v-bind:style="{background: background_colour, borderColor: border_colour}">
  {{ number }}
</td>
`
});


Vue.component('gems-list', {
    props: {gems: {},
            title: "",
            display_zeros: {default: true}},
    template: `
<div class="gems-list">
    <h3 v-if="title">{{ title }}</h3>
    <ul>
    <gem-counter 
        v-for="(number, colour) in gems"
        v-bind:key="colour"
        v-bind:colour="colour"
        v-bind:number="number"
        v-if="number > 0 || display_zeros">
    </gem-counter>
    </ul>
</div>`
});

Vue.component('gem-counter', {
    props: ['colour', 'number'],
    computed: {
        border_colour: function() {
            return border_colours[this.colour];
        },
        background_colour: function() {
            return background_colours[this.colour];
        }
    },
    template: `
<li class="gem-counter" 
    v-bind:style="{background: background_colour, borderColor: border_colour}">
  {{ number }}
</li>
`
});

Vue.component('move-maker', {
    props: ['player', 'supply_gems'],
    template: `
<div class="move-maker">
  <gem-selector v-bind:supply_gems="supply_gems">
  </gem-selector>
</div>
`
});

Vue.component('gem-selector', {
    props: ['supply_gems'],
    data: function() {
        return {
            gems: {white: 0,
                   blue: 0,
                   green: 0,
                   red: 0,
                   black: 0,
                   gold: 0},
        };
    },
    computed: {
        can_increment: function() {
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
            // var incrementable = {white: (this.supply_gems['white'] > 0),
            //                      blue: (this.supply_gems['blue'] > 0),
            //                      green: (this.supply_gems['green'] > 0),
            //                      red: (this.supply_gems['red'] > 0),
            //                      black: (this.supply_gems['black'] > 0),
            //                      gold: (this.supply_gems['gold'] > 0)};
            var incrementable = {};
            for (var i = 0; i < colours.length; i++) {
                var colour = colours[i];
                incrementable[colour] = !any_value_2 && (
                    (num_values_1 == 1 && this.gems[colour] == 1 && this.supply_gems[colour] > 1) || 
                        ((num_values_1 < 3) && this.supply_gems[colour] > 0 && this.gems[colour] == 0));
            }
            return incrementable;
        },
        can_decrement: function() {
            var decrementable = {};
            for (var i = 0; i < colours.length; i++) {
                var colour = colours[i]
                decrementable[colour] = (this.gems[colour] > 0);
            }
            return decrementable;
        }
    },
    template: `
<table class="gem-selector">
  <tr>
    <gems-table-gem-counter v-for="(number, colour) in gems"
        v-bind:key="colour"
        v-bind:colour="colour"
        v-bind:number="number">
    </gems-table-gem-counter>
  </tr>
  <tr>
    <increment-button v-for="(number, colour) in gems"
                      v-bind:key="colour"
                      v-bind:enabled="can_increment[colour]"
                      v-on:increment="gems[$event] += 1"
                      v-bind:colour="colour">
    </increment-button>
  </tr>
  <tr>
    <decrement-button v-for="(number, colour) in gems"
                      v-bind:key="colour"
                      v-bind:enabled="can_decrement[colour]"
                      v-on:decrement="gems[$event] -= 1"
                      v-bind:colour="colour">
    </decrement-button>
  </tr>
</table>
`
});

Vue.component('increment-button', {
    props: ['colour', 'enabled'],
    template: `
<td class="increment-button">
  <button v-bind:disabled="!enabled"
          v-on:click="$emit('increment', colour)">
    +
  </button>
</td>
`
});

Vue.component('decrement-button', {
    props: ['colour', 'enabled'],
    template: `
<td class="decrement-button">
  <button v-bind:disabled="!enabled"
          v-on:click="$emit('decrement', colour)">
    -
  </button>
</td>
`
});

Vue.component('player-display', {
    props: ['player'],
    computed: {
        player_num_gems: function() {
            return (this.player.gems['white'] +
                    this.player.gems['blue'] +
                    this.player.gems['green'] +
                    this.player.gems['red'] +
                    this.player.gems['black'] +
                    this.player.gems['gold']);
        }
    },
    template: `
<div class="player-display">
<h3>Player {{ player.number }}: {{ player.score }} points, {{ player_num_gems }} gems</h3>
    <gems-table v-bind:gems="player.gems"
                v-bind:show_card_count="true"
                v-bind:cards="player.card_colours">
    </gems-table>
    <cards-display v-bind:cards="player.cards_in_hand"
                   v-bind:player="player"
                   v-bind:show_reserve_button="false">
    </cards-display>
</div>
`
})

Vue.component('cards-display', {
    props: ['cards', 'name', 'player', 'show_reserve_button'],
    template: `
<div class="cards-display">
    <h3>{{ name }}</h3>
    <ul class="single-line-list">
      <card-display
          v-for="card in cards"
          v-bind:show_reserve_button="show_reserve_button"
          v-bind:player="player"
          v-bind:key="card.id"
          v-bind:card="card" >
      </card-display>
    </ul>
</div>
`
})

Vue.component('card-display', {
    props: ['card', 'player', 'show_reserve_button'],
    computed: {
        background_colour: function() {
            return background_colours[this.card.colour];
        },
        buyable: function() {
            return this.player.can_afford(this.card);
        },
        reservable: function() {
            return (this.player.cards_in_hand.length <= 3);
        }
    },
    template: `
<li class="card-display">
<div class="card-display-contents" v-bind:style="{background: background_colour}">
    <p class='card-points'>{{ card.points }}</p>
    <button v-if="show_reserve_button"
            v-bind:disabled="!reservable">
        reserve
    </button>
    <button v-bind:disabled="!buyable">
        buy
    </button>
    <gems-list v-bind:gems="card.gems" 
               v-bind:display_zeros="false">
    </gems-list>
</div>
</li>
`
})

var app = new Vue({
    el: '#app',
    data: {
        state: test_state,
        supply_gems: test_state.supply_gems,
        players: test_state.players
    },
    methods: {
        testChangeGems: function() {
            this.state.reduce_gems();
        },
        reset: function() {
            this.state = new GameState();
        } 
    },
    computed: {
        human_player: function() {
            return this.state.players[0];
        },
        round_number: function() {
            return this.state.round_number;
        }
    }
});

