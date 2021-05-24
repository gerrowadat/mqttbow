
import enum
import asyncio
import importlib


class KeyInterfaceError(Exception):
    pass


class KeyStateError(KeyInterfaceError):
    pass


class Implementation(enum.Enum):
    # Actually usee the keybow
    KEYBOW = 1
    # Do a simulated set of things, once.
    SIMULATED = 2
    # Don't do anything
    DUMMY = 3


class KeyState(object):
    def __init__(self):
        self._pressed = False
        self._r = 0
        self._g = 0
        self._b = 0

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, var):
        if var not in (True, False):
            raise KeyStateError('pressed must be True/False, not %s' % (type(var), ))
        self._pressed = var

    def down(self):
        self._pressed = True

    def up(self):
        self.pressed = False

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, var):
        try:
            self._r = int(var)
        except TypeError:
            raise KeyStateError('color value must be an int')

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, var):
        try:
            self._g = int(var)
        except TypeError:
            raise KeyStateError('color value must be an int')

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, var):
        try:
            self._b = int(var)
        except TypeError:
            raise KeyStateError('color value must be an int')

    @property
    def colourcode(self):
        return '%s%s%s' % (self.r, self.g, self.b)

    def clear(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def __str__(self):
        return '[%s] : %s' % ('X' if self.pressed else ' ', self.colourcode)


class KeyInterface(object):
    def __init__(self, impl=Implementation.KEYBOW):
        self._impl = impl
        self._state = {}
        self._handlers = None
        self._last_show = None
        self._keybow = None
        self._last_press = None

        if self._impl == Implementation.KEYBOW:
            try:
                self._keybow = importlib.import_module('keybow')
            except ModuleNotFoundError:
                raise KeyInterfaceError('keybow python module not installed')

    def setup(self, keycount=3):
        for k in range(keycount):
            self._state[k] = KeyState()
        if self._impl == Implementation.KEYBOW:
            self._keybow.setup(self._keybow.MINI)

            def _handler(idx, state):
                self.update(idx, state)

            for idx in range(keycount):
                self._handler = self._keybow.on(index=idx, handler=_handler)

    def update(self, idx, state):
        self._state[idx].pressed = state
        self._last_press = (idx, state)

    def show(self):
        if self._impl == Implementation.KEYBOW:
            self._keybow.show()
        elif self._impl == Implementation.SIMULATED:
            if self._state != self._last_show:
                self._last_show = self._state
                for k in self._state:
                    print('[%d %s]\n' % (k, str(self._state[k])))

    def clear(self):
        if self._impl == Implementation.KEYBOW:
            self._keybow.clear()
        for k in self._state:
            self._state[k].clear()

    async def async_wait(self):
        while True:
            last = self._last_press
            if last:
                self._last_press = None
                return last
            await asyncio.sleep(1.0 / 120.0)
