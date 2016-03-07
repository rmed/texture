# Scenarios

Writing your scenarios is a very simple task. In order to keep things clean,
texture expects every scenario to be found in a single class per file. This
class has to be named `Scenario`, and the module name (`NAME.py`) will be used
as reference to that scenario.

Each scenario must implement (at least) these two methods:

- `load()`: executed when changing scenario. This is normally used to print
  scenario description or make some special initialization
- `do_action(cmd)`: receives user input and executes an action

In addition, the `Scenario` class has access to the game state dictionary, so
you may use that, for instance, to get/set flags.

**Note:** the first scenario that is loaded automatically must be named `start`.

## Scenario example

~~~python
import texture

class Scenario(texture.BaseScenario):

    def load(self):
        if self.state.get('in_start', False):
            # Start of the game
            print('Started the game')
            self.state['in_start'] = True

        else:
            # Already been here
            print('You have already been here')

    def do_action(self, cmd):
        if cmd == 'go south':
            print('You go south')

            # Load different scenario
            return 'load south'

        elif cmd == 'go north':
            print ('You go north')

            # Load different scenario
            return 'load north'

        else:
            # Unrecognized command
            print('What are you doing!?')

            # Optinonally, continue main game loop
            return 'continue'
~~~

Note that the `do_action()` method can return `load X` to load scenario X and
`continue` to continue with the next iteration of the main loop (for whatever
reason).

However, the `util` module offers a better way to do this:

- Instead of `return 'load X'`, you can use `return texture.loader('X')`
- Instead of `return 'continue'`, you can use `return texture.dotick`

These two alternatives are recommended when using decorators to print text.
