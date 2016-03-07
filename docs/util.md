# Utilities

texture includes some utilities for writing scenarios.

## `loader`

Useful for loading scenarios in the game master, and as an alternative to
writing `return 'load X'`. It is very easy to use:

~~~python
from texture import loader

# class Scenario...

    def do_action(self, cmd):
        if cmd == 'go north':
            return loader('north')
~~~

---

## `dotick`

Useful for continuing with next iteration of the main game loop, and as an
alternative to writing `return 'continue'`:

~~~python
from texture import dotick

# class Scenario...

    def do_action(self, cmd):
        if cmd == 'pass':
            # Maybe do something here that changes the state?
            return dotick
~~~

---

## `tclear()`

Clear the screen.

---

## `tnewline(times=1)`

Prints the newline character the number of times specified.

---

## `tprint(text, dedent=True)`

Prints text on screen. The `dedent` parameter is used to specify whether the
text should be dedented and remove all blank spaces before the text (True) or
should keep the indentation (False).

---

## `@printer`

Decorator function that will print strings that are returned from the decorated
function. Calls `tprint()` internally, so you can also supply the `dedent`
parameter:

~~~python
from texture import printer

# class Scenario...

    @printer
    def do_action(self, cmd):
        if cmd == 'look':
            return 'You look around and find nothing of interest'
~~~
