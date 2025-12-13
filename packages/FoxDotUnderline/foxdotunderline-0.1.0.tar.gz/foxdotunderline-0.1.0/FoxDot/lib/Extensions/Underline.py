"""Stop through the underline."""

from FoxDot.lib.Code import FoxDotCode
from FoxDot.lib.Players import Group


class Underline:
    """Stop through the underline.

    Just put a _ before or after the player's name.

    Examples
    --------
    # Stop from the Synth startup
    >>> _d1 >> bass()
    >>> d1_ >> bass()

    # Stop from the change of an attribute
    >>> _d1.oct=5
    >>> d1_.oct=5

    # Stop from the use of a player method
    >>> _d1.every(2, 'jump')
    >>> d1_.every(2, 'jump')

    # Stop a synth that has ~ ahead
    >>> ~_d1 >> bass()
    >>> ~d1_ >> bass()

    # Stop by printing it, turning it into a string or getting for its repr
    >>> print(_d1_all)
    >>> str(d1_all_)
    >>> repr(d1_all_)
    """

    def __init__(self, player):
        super().__setattr__('player', player)

    def _stop(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.player.stop()
        return f'{self.player.id}.stop()'

    def __getattr__(self, name):
        attr = getattr(self.player, name)
        self._stop()
        return attr

    def __invert__(self):
        return self

    __str__ = __repr__ = __rshift__ = __setattr__ = _stop


# Instantiates all two-character variable Underline Objects
_alphabet = 'abcdefghijklmnopqrstuvwxyz'
_numbers  ='0123456789'

_underlines = {}

for _char1 in _alphabet:
    for _char2 in _alphabet + _numbers:
        _name = _char1 + _char2
        _under = Underline(FoxDotCode.namespace[_name])
        for _key in [f'_{_name}', f'{_name}_']:
            _underlines[_key] = _under

    _name = f'{_char1}_all'
    _under_all = Underline(FoxDotCode.namespace[_name])
    for _key in [f'_{_name}', f'{_name}_']:
        _underlines[_key] = _under_all

globals().update(_underlines)

__all__ = list(_underlines)
