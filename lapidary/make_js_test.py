
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


''')

def make_test_state(state):
    output = template.render(
        colours=colours,
        all_colours=all_colours,
        s=state)

    return output
