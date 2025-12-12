# vertical-python

Python but vertical.

Write a `.vpy` file:

`hello_world.vpy`
```
h d
e e
l f
l
oph
_re
wil
onl
rto
l(_
d"w
(ho
)er
 ll
 ld
 o(
  )
 w:
 o
 r
 l
 d
 !
 "
 )
```

then run it

```bash
$ vertical-python ./hello_world.vpy
hello world!
```

or encode a `.py` file to a `.vpy` file:

```bash
$ vertical-python ./hello_world.vpy --print > hello_world.py
$ vertical-python --encode ./hello_world.py > hello_world.vpy
```

## Imports

To make your vertical python file importable, use the `.py` file extension and [declare a `vertical` encoding](https://peps.python.org/pep-0263/)

The `vertical_python.codec` module must be imported before attempting to import vertically-encoded python.

```
# -*- coding=vertical -*-
p
r
i
n
t
(
"
n
e
a
t
!
"
)
```

## CLI

```
usage: vertical-python [-h] [--print | --encode] path

python but vertical

positional arguments:
  path        path to vertical .vpy file

options:
  -h, --help  show this help message and exit
  --print     just print the rotated vpy, not eval
  --encode    treat PATH as .py and print vertical .vpy to stdout

```

## Changelog

- v0.3.0: [`#2`](https://github.com/sneakers-the-rat/vertical-python/pull/2) - `vertical` codec and importable modules
- v0.2.0: [`#1`](https://github.com/sneakers-the-rat/vertical-python/pull/1) - [@mathematicalmichael](https://github.com/mathematicalmichael) - encode `.py` to `.vpy` 
- v0.1.0: Initial functionality