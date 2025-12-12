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

## CLI

```
usage: vertical-python [-h] [--print] path

python but vertical

positional arguments:
  path        path to vertical .vpy file

options:
  -h, --help  show this help message and exit
  --print     just print the rotated vpy, not eval

```