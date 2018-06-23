
import jinja2 as jin
from data import colours, all_colours

template = jin.Template('''
s = new GameState({{ s.num_players }});

s.current_player_index = {{ s.current_player_index }};

{% for player in s.players %}
s.players[{{ loop.index0 }}].gems = {
  {% for colour in all_colours %}
    {{ colour }}: {{ player.num_gems(colour) }}{% if not loop.last %},{% endif %}
  {% endfor %}
};
{% endfor %}

s.supply_gems = {
  {% for colour in all_colours %}
    {{ colour }}: {{ s.num_gems_available(colour) }}{% if not loop.last %},{% endif %}
  {% endfor %}
}


{% for player in s.players %}
s.players[{{ loop.index0 }}].cards_in_hand = [
  {% for card in player.cards_in_hand %}
     new Card({{ card.tier }}, '{{ card.colour }}', {{ card.points }}, { {% for colour in colours %}{{ colour }}: {{ card.num_required(colour) }}{% if not loop.last %},{% endif %} {% endfor %} } ){% if not loop.last %},{% endif %}
  {% endfor %}
];
{% endfor %}


{% for player in s.players %}
s.players[{{ loop.index0 }}].card_colours = {
  {% for colour in colours %}
    {{ colour }}: {{ player.num_cards_of_colour(colour) }}{% if not loop.last %},{% endif %}
  {% endfor %}
};
{% endfor %}

{% for player in s.players %}
s.players[{{ loop.index0 }}].score = {{ player.score }};
{% endfor %}

{% for player in s.players %}
s.players[{{ loop.index0 }}].cards_played = [
  {% for card in player.cards_played %}
     new Card({{ card.tier }}, '{{ card.colour }}', {{ card.points }}, { {% for colour in colours %}{{ colour }}: {{ card.num_required(colour) }}{% if not loop.last %},{% endif %} {% endfor %} } ){% if not loop.last %},{% endif %}
  {% endfor %}
];
{% endfor %}

{% for player in s.players %}
s.players[{{ loop.index0 }}].nobles = [
  {% for noble in player.nobles %}
     new Noble({ {% for colour in colours %}{{ colour }}: {{ noble.num_required(colour) }}{% if not loop.last %},{% endif %} {% endfor %} } ){% if not loop.last %},{% endif %}
  {% endfor %}
];
{% endfor %}

s.nobles = [
  {% for noble in s.nobles %}
     new Noble({ {% for colour in colours %}{{ colour }}: {{ noble.num_required(colour) }}{% if not loop.last %},{% endif %} {% endfor %} } ){% if not loop.last %},{% endif %}
  {% endfor %}
];


{% for tier in range(1, 4) %}
s.cards_in_market[{{ tier }}] = [
  {% for card in s.cards_in_market(tier) %}
     new Card({{ card.tier }}, '{{ card.colour }}', {{ card.points }}, { {% for colour in colours %}{{ colour }}: {{ card.num_required(colour) }}{% if not loop.last %},{% endif %} {% endfor %} } ){% if not loop.last %},{% endif %}
  {% endfor %}
];
{% endfor %}

v0 = state_vector(s, 0);
v1 = state_vector(s, 1);

v0_python = {{ s.get_state_vector(0).tolist() }};
v1_python = {{ s.get_state_vector(1).tolist() }};


console.log('Testing state');
for (let i = 0; i < v0.length; i++) {
    if (v0[i] != v0_python[i]) {
        console.log('v0 mismatch at', i);
    }
    if (v1[i] != v1_python[i]) {
        console.log('v1 mismatch at', i);
    }

}
''')

def make_test_state(state):
    output = template.render(
        colours=colours,
        all_colours=all_colours,
        s=state)

    return output
