
Lapidary AI
===========

An AI for the board game Splendor, using a simple neural let trained
with reinforcement learning.

The ``lapidary`` folder contains the Python code used to train the
network. It currently depends on Tensorflow.

`lapidary/tui.py` provides a simple terminal gui for the
game, useful for quickly testing current networks.

`webgui` provides a web gui, reimplementing the game logic in
javascript and implementing the neural net by directly evaluating the
matrix mathematics. It depends on weights exported from the Python code.
