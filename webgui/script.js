
class Player {
    constructor() {
        this.cards_in_hand = [];
        this.cards_played = [];
        this.nobles = [];

        this.gems = {white: 0,
                     blue: 0,
                     green: 0,
                     red: 0,
                     black: 0,
                     gold: 0};

        this.score = 0;
    }

    num_gems(colour) {
        return this.gems[colour];
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
            this.players.push(new Player());
        }
        
    }

    reduce_gems() {
        this.supply_gems['green'] -= 2;
        this.supply_gems['blue'] += 1;
        this.players[0].score += 1;
    }
}

var test_state = new GameState();


Vue.component('gems-list', {
    props: ['gems', 'title'],
    template: `
<div class="gem-counter">
    <h3>{{ title }}</h3>
    <ul>
    <gem-counter 
        v-for="(number, colour) in gems"
        v-bind:key="colour"
        v-bind:colour="colour"
        v-bind:number="number">
    </gem-counter>
    </ul>
</div>`
});

Vue.component('gem-counter', {
    props: ['colour', 'number'],
    template: `
<li v-bind:style="{color: colour}">
  {{ colour }} = {{ number }}
</li>`
});

Vue.component('player-display', {
    props: ['player'],
    template: `
<p class="player-display">{{ player }}</p>
`
})

var app = new Vue({
    el: '#app',
    data: {
        supply_gems: test_state.supply_gems,
        players: test_state.players
    },
    methods: {
        testChangeGems: function() {
            test_state.reduce_gems();
        }
    }
});

