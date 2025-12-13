===================
Using Jambo
===================

Jambo is designed to be easy to use. It doesn't require complex setup or configuration when not needed, while providing more powerful instance methods when you do need control.

Below is an example of how to use Jambo to convert a JSON Schema into a Pydantic model.


-------------------------
Static Method (no config)
-------------------------

.. code-block:: python

    from jambo import SchemaConverter

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

    Person = SchemaConverter.build(schema)

    obj = Person(name="Alice", age=30)
    print(obj)
    # Output: Person(name='Alice', age=30)


The :py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>` static method takes a JSON Schema dictionary and returns a Pydantic model class.

Note: the static ``build`` method was the original public API of this library. It creates and returns a model class for the provided schema but does not expose or persist an instance cache.


--------------------------------
Instance Method (with ref cache)
--------------------------------

.. code-block:: python

    from jambo import SchemaConverter

    converter = SchemaConverter()

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

    # The instance API (build_with_cache) populates the converter's instance-level reference cache
    Person = converter.build_with_cache(schema)

    obj = Person(name="Alice", age=30)
    print(obj)
    # Output: Person(name='Alice', age=30)

    # When using the converter's built-in instance cache (no ref_cache passed to the call),
    # all object types parsed during the build are stored and can be retrieved via get_cached_ref.

    cached_person_model = converter.get_cached_ref("Person")
    assert Person is cached_person_model  # the cached class is the same object that was built

    # A nested/subobject type can also be retrieved from the instance cache
    cached_address_model = converter.get_cached_ref("Person.address")


The :py:meth:`SchemaConverter.build_with_cache <jambo.SchemaConverter.build_with_cache>` instance method was added after the
initial static API to make it easier to access and reuse subtypes defined in a schema.
Unlike the original static :py:meth:`SchemaConverter.build <jambo.SchemaConverter.build>`,
the instance method persists and exposes the reference cache and provides helpers such as
:py:meth:`SchemaConverter.get_cached_ref <jambo.SchemaConverter.get_cached_ref>` and
:py:meth:`SchemaConverter.clear_ref_cache <jambo.SchemaConverter.clear_ref_cache>`.

.. warning::
    The instance API with reference cache can lead to schema and type name collisions if not managed carefully.
    It's recommended that each schema defines its own unique namespace using the `$id` property in JSON Schema,
    and then access it's ref_cache by passing it explicitly when needed.
    
For details and examples about the reference cache and the different cache modes (instance cache, per-call cache, ephemeral cache), see:

.. toctree::
    usage.ref_cache


Type System
-----------

For a full explanation of the supported schemas and types see our documentation on types:

.. toctree::
    :maxdepth: 2

    usage.string
    usage.numeric
    usage.bool
    usage.array
    usage.object
    usage.reference
    usage.allof
    usage.anyof
    usage.oneof
    usage.enum
    usage.const