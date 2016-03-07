# Project structure

A basic game will have a structure similar to:

~~~
game.py
scenarios/
    __init__.py
    scenario1.py
    scenario2.py
~~~

By default, the `scenarios` directory will be treated as a module and the
scenarios inside imported automatically on startup (although you can specify
the name of the module to use).

The `game.py` file would contain all the logic and instructions necessary for
configuring and starting the `GameMaster` (you can change the name of this file
freely).
