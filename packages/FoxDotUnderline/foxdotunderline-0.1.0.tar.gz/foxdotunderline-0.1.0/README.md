# FoxDotUnderline - Stop through the underline

Just put a _ before or after the player's name.

``` python
_d1 >> bass()
```

## Instalation

``` shell
pip install FoxDotUnderline
# or
pip install git+https://codeberg.org/FoxDotExtensions/FoxDotUnderline
```

## Usage

Import lib

``` python
from FoxDot.lib.Extensions.Underline import *
```

Stop from the Synth startup

``` python
_d1 >> bass()
d1_ >> bass()
```

Stop from the change of an attribute

``` python
_d1.oct=5
d1_.oct=5
```

Stop from the use of a player method

``` python
_d1.every(2, 'jump')
d1_.every(2, 'jump')
```

Stop a synth that has `~` ahead

``` python
~_d1 >> bass()
~d1_ >> bass()
```

Stop by printing it, turning it into a string or getting for its repr

``` python
print(_d1_all)
str(d1_all_)
repr(d1_all_)
```
