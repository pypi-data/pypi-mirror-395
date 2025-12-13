===============
Reference Cache
===============

The reference cache is named after the mechanism used to implement
the `$ref` keyword in the JSON Schema specification.

Internally, the cache is used by both :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>`
and :py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>`.
However, only :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>` exposes the cache through a supported API;
:py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>` uses the cache internally and does not provide access to it.

The reference cache accepts a mutable mapping (typically a plain Python dict)
that maps reference names (strings) to generated Pydantic model classes.
Since only the reference names are stored it can cause name collisions if
multiple schemas with overlapping names are processed using the same cache.
Therefore, it's recommended that each namespace or schema source uses its own
:class:`SchemaConverter` instance.

-----------------------------------------
Configuring and Using the Reference Cache
-----------------------------------------

The reference cache can be used in three ways:

* Without a persistent reference cache (no sharing between calls).
* Passing an explicit ``ref_cache`` dictionary to a call.
* Using the converter instance's default cache (the instance-level cache).


Usage Without Reference Cache
=============================

When you run the library without a persistent reference cache, the generated
types are not stored for reuse. Each call to a build method creates fresh
Pydantic model classes (they will have different Python object identities).
Because nothing is cached, you cannot look up generated subtypes later.

This is the default behaviour of :py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>`.
You can achieve the same behaviour with :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>` by
passing ``without_cache=True``.


Usage: Manually Passing a Reference Cache
=========================================

You can create and pass your own mutable mapping (typically a plain dict)
as the reference cache. This gives you full control over sharing and
lifetime of cached types. When two converters share the same dict, types
created by one converter will be reused by the other.

.. code-block:: python

    from jambo import SchemaConverter

    # a shared cache you control
    shared_cache = {}

    converter1 = SchemaConverter(shared_cache)
    converter2 = SchemaConverter(shared_cache)

    model1 = converter1.build_with_cache(schema)
    model2 = converter2.build_with_cache(schema)

    # Because both converters use the same cache object, the built models are the same object
    assert model1 is model2

If you prefer a per-call cache (leaving the converter's instance cache unchanged), pass the ``ref_cache`` parameter to
:py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>`:

.. code-block:: python

    # pass an explicit, private cache for this call only
    model_a = converter1.build_with_cache(schema, ref_cache={})
    model_b = converter1.build_with_cache(schema, ref_cache={})

    # because each call received a fresh dict, the resulting model classes are distinct
    assert model_a is not model_b


Usage: Using the Instance Default (Instance-level) Cache
=======================================================

By default, a :class:`SchemaConverter` instance creates and keeps an internal
reference cache (a plain dict). Reusing the same converter instance across
multiple calls will reuse that cache and therefore reuse previously generated
model classes.

That cache is isolated per namespace via the `$id` property in JSON Schema, so
schemas with different `$id` values will not collide in the same cache.

.. code-block:: python

    from jambo import SchemaConverter

    # no $id in this example, therefore a default namespace is used
    schema = {
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                },
                "required": ["street", "city"],
            },
        },
        "required": ["name", "address"],
    }

    converter = SchemaConverter()  # has its own internal cache

    model1 = converter.build_with_cache(schema)
    model2 = converter.build_with_cache(schema)

    # model1 and model2 are the same object because the instance cache persisted
    assert model1 is model2

When passing a schema with a different `$id`, the instance cache keeps types
separate:

.. code-block:: python

    schema_a = {
        "$id": "namespace_a",
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }

    schema_b = {
        "$id": "namespace_b",
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }

    converter = SchemaConverter()  # has its own internal cache

    model_a = converter.build_with_cache(schema_a)
    model_b = converter.build_with_cache(schema_b)

    # different $id values isolate the types in the same cache
    assert model_a is not model_b

If you want to temporarily avoid using the instance cache for a single call,
use ``without_cache=True``. That causes :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>` to
use a fresh, empty cache for the duration of that call only:

.. code-block:: python

    model1 = converter.build_with_cache(schema, without_cache=True)
    model2 = converter.build_with_cache(schema, without_cache=True)

    # each call used a fresh cache, so the models are distinct
    assert model1 is not model2


Inspecting and Managing the Cache
=================================

The converter provides a small, explicit API to inspect and manage the
instance cache.

Retrieving cached types
-----------------------

:py:meth:`SchemaConverter.get_cached_ref <jambo.SchemaConverter.get_cached_ref>`(name, namespace="default") — returns a cached model class or ``None``.

Retrieving the root type of the schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When retrieving the root type of a schema, pass the schema's ``title`` property as the name.

.. code-block:: python

    from jambo import SchemaConverter

    converter = SchemaConverter()

    schema = {
        "title": "person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
    }

    person_model = converter.build_with_cache(schema)
    cached_person_model = converter.get_cached_ref("person")


Retrieving a subtype
~~~~~~~~~~~~~~~~~~~~

When retrieving a subtype, pass a path string (for example, ``parent_name.field_name``) as the name.

.. code-block:: python

    from jambo import SchemaConverter

    converter = SchemaConverter()

    schema = {
        "title": "person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                },
                "required": ["street", "city"],
            },
        }
    }

    person_model = converter.build_with_cache(schema)
    cached_address_model = converter.get_cached_ref("person.address")



Retrieving a type from ``$defs``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When retrieving a type defined in ``$defs``, access it directly by its name.

.. code-block:: python

    from jambo import SchemaConverter

    converter = SchemaConverter()

    schema = {
        "title": "person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "address": {"$ref": "#/$defs/address"},
        },
        "$defs": {
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                },
                "required": ["street", "city"],
            }
        },
    }

    person_model = converter.build_with_cache(schema)
    cached_address_model = converter.get_cached_ref("address")


Isolation by Namespace
~~~~~~~~~~~~~~~~~~~~~~

The instance cache is isolated per namespace via the `$id` property in JSON Schema.
When retrieving a cached type, you can specify the namespace to look in
(via the ``namespace`` parameter). By default, the ``default`` namespace is used


.. code-block:: python

    from jambo import SchemaConverter

    converter = SchemaConverter()

    schema_a = {
        "$id": "namespace_a",
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }

    schema_b = {
        "$id": "namespace_b",
        "title": "Person",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }

    person_a = converter.build_with_cache(schema_a)
    person_b = converter.build_with_cache(schema_b)

    cached_person_a = converter.get_cached_ref("Person", namespace="namespace_a")
    cached_person_b = converter.get_cached_ref("Person", namespace="namespace_b")

    assert cached_person_a is person_a
    assert cached_person_b is person_b


Clearing the cache
------------------

:py:meth:`SchemaConverter.clear_ref_cache <jambo.SchemaConverter.clear_ref_cache>`(namespace: Optional[str]="default") — removes all entries from the instance cache.


When you want to clear the instance cache, use :py:meth:`SchemaConverter.clear_ref_cache <jambo.SchemaConverter.clear_ref_cache>`.
You can optionally specify a ``namespace`` to clear only that namespace;
otherwise, the default namespace is cleared.

If you want to clear all namespaces, call :py:meth:`SchemaConverter.clear_ref_cache <jambo.SchemaConverter.clear_ref_cache>` passing `None` as the namespace,
which removes all entries from all namespaces.


Notes and Behavioural Differences
================================

* :py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>` does not expose or persist an instance cache. If you call it without
  providing a ``ref_cache`` it will create and use a temporary cache for that
  call only; nothing from that call will be available later via
  :py:meth:`SchemaConverter.get_cached_ref <jambo.SchemaConverter.get_cached_ref>`.

* :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>` is the supported entry point when you want
  cache control: it uses the instance cache by default, accepts an explicit
  ``ref_cache`` dict for per-call control, or uses ``without_cache=True`` to
  run with an ephemeral cache.


References in the Test Suite
============================

These behaviours are exercised in the project's tests; see :mod:`tests.test_schema_converter`
for examples and additional usage notes.
