# -*- coding: utf-8 -*-
#
# texture game engine
# https://github.com/rmed/texture
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Rafael Medina García <rafamedgar@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from  . import util
from six.moves import input
import pkgutil
import readline
import six
import sys


class GameMaster(object):
    """
        Attributes:

            current         - current Scenario instance
            game_commands   - dict that contains special commands,
                which are parsed before those of the curent Scenario,
                and the functions they execute
            state           - global game state shared and updated on each
                Scenario load
            scenarios       - map of scenarios
    """

    def __init__(self, scenarios='scenarios'):
        """ Object that implements the main game loop and the command input.

            scenarios   - name of the module that contains the scenarios.
                These scenarios are imported at startup automatically.
        """
        self.current = None
        self.game_commands = {}
        self.state = {}

        # Import scenarios
        self.scenarios = {}

        pkg = sys.modules[scenarios]
        for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
            try:
                mod = __import__('%s.%s' % (scenarios, modname),
                    fromlist=['Scenario'])
                self.scenarios[modname] = mod.Scenario

            except ImportError:
                util.tprint('Failed to import' + modname)
                continue

            except AttributeError:
                util.tprint('Module "%s" is not a scenario' % modname)
                continue

    def start_game(self):
        """ Call the main loop. """
        self._main_loop()

    def register_command(self, cmd, func):
        """ Register a game command.

            These commands are parsed before the scenario actions and may be
            used to perform special action such as restarting the game or
            loading a special scenario.

            These commands may return special strings to perform actions
            in the game loop:

                continue - next "game tick"
                load X   - load another scenario

            cmd  - command to match
            func - function to execute
        """
        self.game_commands[cmd] = func

    def _change_scenario(self, name):
        """ Change scenario and call the scenario `load()` method.

            Substitutes the `self.current` reference to point to the new
            scenario.

            name - name of the scenario in the scenarios map
        """
        # Update state
        if self.current:
            self.state = self.current.state

        scenario = self.scenarios.get(name, None)

        if not scenario:
            util.tprint('[ERROR] Scenario "%s" not found' % name)
            return

        self.current = scenario(self.state)
        self.current.load()

    def _exec_game_command(self, cmd):
        """ Try to match user input to a game command and execute its
            function if found.
        """
        func = self.game_commands.get(cmd, None)

        if not func:
            return None

        return func(self.state)

    def _main_loop(self):
        """ Main game loop. """
        # First scenario is 'start'
        sc_name = 'start'
        self._change_scenario(sc_name)

        while True:
            # Ask for input
            util.tnewline()
            cmd = input('> ')
            util.tnewline()

            # Preset game commands
            response = self._exec_game_command(cmd)

            if not response:
                # Perform scenario action
                response = self.current.do_action(cmd)

            # Parse response
            if isinstance(response, util.TickUtil):
                continue

            elif isinstance(response, util.LoaderUtil):
                sc_name = response.scenario
                self._change_scenario(sc_name)

            elif isinstance(response, six.text_type):
                # Game loop commands
                if response == 'continue':
                    continue

                elif response.startswith('load'):
                    sc_name = response.split('load')[1].strip()
                    self._change_scenario(sc_name)
