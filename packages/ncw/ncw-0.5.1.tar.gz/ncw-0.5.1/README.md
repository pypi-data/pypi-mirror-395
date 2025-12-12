# ncw

_Nested collections wrapper_

Classes to access and/or modify data in nested collections (**dict** or **list** instances)
of **str**, **int**, **float**, **bool**, or `None`, through a [Mapping] or
[MutableMapping] interface using direct addressing.


## Usage

Use the **FrozenStructure** class to access data in nested collections by either
a string comprised of the segments of the keys or indexes in the "path" addressing the
substructure or value, joined together by a separator character
(usually an ASCII dot: `.`), or a tuple of these path segments.

``` pycon
>>> serialized = '{"herbs": {"common": ["basil", "oregano", "parsley", "thyme"], "disputed": ["anise", \
"coriander"]}}'
>>>
>>> import json
>>> original_data = json.loads(serialized)
>>>
>>> from ncw import FrozenStructure
>>> readonly = FrozenStructure.from_native(original_data)
>>>
>>> readonly["herbs"]
{'common': ['basil', 'oregano', 'parsley', 'thyme'], 'disputed': ['anise', 'coriander']}
>>> readonly["herbs.common"]
['basil', 'oregano', 'parsley', 'thyme']
>>> readonly["herbs", "common"]
['basil', 'oregano', 'parsley', 'thyme']
>>> readonly["herbs.common.1"]
'oregano'
>>> readonly["herbs", "common", 1]
'oregano'
```

The **MutableStructure** class additionally allows changes to the stored data,
see the [documentation] for more details.

* * *
[Mapping]: https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping
[MutableMapping]: https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping
[documentation]: https://blackstream-x.gitlab.io/ncw
