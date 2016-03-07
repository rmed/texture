# The game launcher

The *game launcher* is the startup script for your game (aka: what you execute
in order to play) and serves as the entrypoint that configures the `GameMaster`
and runs the main loop.

## Simple example

A really simple example of a *game launcher* would be:

~~~python
import texture

if __name__ == '__main__':
    gm = texture.GameMaster()

    # Start main loop
    gm.start_game()
~~~

This simple script will import all the modules in the default directory/module
`scenario` and load the one named `start` when done. Following sections will
show how to fine-tune this launcher.

---

## Changing the scenarios module

If for whatever reason you don't want to use the default `scenarios` module,
you may specify your own module as so:

~~~python
import texture

if __name__ == '__main__':
    # Do not use default scenarios module
    gm = texture.GameMaster(scenarios='potato')

    # Start main loop
    gm.start_game()
~~~

---

## Adding special global commands

There will be times where you want some commands available in all your
scenarios. The `GameMaster` includes a nice method for doing just that:

~~~python
import texture
import sys

def exit_game(state): # State will be passed to the function automatically
    sys.exit('Thanks for playing!')

if __name__ == '__main__':
    gm = texture.GameMaster()

    # Register special command
    gm.register_command('EXIT', game_exit)

    gm.start_game()
~~~

Now, the `EXIT` command will be available in every scenario you write.
