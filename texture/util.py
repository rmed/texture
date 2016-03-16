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

from six.moves import range
import six
import textwrap


class LoaderUtil(object):
    """ Class used to simplify returning scenario load orders and play nice
        with the `@printer` decorator.

        Generally, this class should not be accessed directly. Instead, use the
        `loader` object defined below. Usage:

            return loader('my_new_scenario')
    """

    def __init__(self):
        self.scenario = ''

    def __call__(self, scenario):
        """ Update the object's scenario to load. """
        if not isinstance(scenario, six.text_type):
            raise TypeError('scenario name should be a string')

        self.scenario = scenario
        return self


class TickUtil(object):
    """ Dummy class for the `dotick` object used to inform the main loop that it
        should continue with the next "tick". As with `LoaderUtil`, this should
        play nice with the `@printer` decorator. Usage:

            return dotick
    """

    def __init__(self):
        pass


# May be used to inform the main loop of the scenario change
loader = LoaderUtil()

# May be used to inform the main loop that it should continue with next tick
dotick = TickUtil()


def tclear():
    """ Clear the screen. """
    six.print_(chr(27) + '[2J')

def tnewline(times=1):
    """ Print the newline character.

        times - number of times to print the character
    """
    for _ in range(0, times):
        six.print_('\n')

def tprint(text, dedent=True):
    """ Print text on screen.

        text    - text to print
        dedent  - whether or not to dedent the text
    """
    if dedent:
        six.print_(textwrap.dedent(text))

    else:
        six.print_(text)

def printer(func=None, **options):
    """ Decorator used to print whatever text is returned in the caller
        function.

        When a list or a tuple are returned, then the contents are iterated
        and printed.

        Options:

            dedent - whether or not to dedent the text (default: True)
    """
    if func:
        def decorator(*args, **kwargs):
            ret = func(*args, **kwargs)
            do_dedent = options.get('dedent', True)

            if not ret:
                # Nothing to print
                return

            if isinstance(ret, six.text_type):
                # Print single text/var
                tprint(ret, do_dedent)

            elif isinstance(ret, tuple) or isinstance(ret, list):
                # Iterate and print all
                for text in ret:
                    tprint(text, do_dedent)


        return decorator

    # Function was not received
    def partial(func):
        return printer(func, **options)

    return partial
