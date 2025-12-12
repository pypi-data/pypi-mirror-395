# fallible
fallible, an experimental ansible

## building
```shell
$ python3 src/fallible/_vendor/_build.py --pr 72553 devel
$ python3 -m build -w -o dist
$ python3 -m build -w -o dist compat_entrypoints
```

Alternatively, instead of using `--pr` to enumerate individual PRs, you can use `--all` to fetch all PRs labeled with `fallible`.

## using
```shell
$ python3 -m fallible playbook site.yml
$ fallible-playbook site.yml
```

## ansible-core compat

The `compat_entrypoints` dir provides a package for `fallible-compat` that will install `ansible*` entrypoints.

```shell
$ pip3 install fallible-compat
$ ansible-playbook site.yml
```
