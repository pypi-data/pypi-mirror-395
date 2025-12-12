Getting started
===============

Installation
------------

.. code-block:: bash

   pip install singlejson

Quickstart
----------

.. code-block:: python

   from singlejson import JSONFile, load, sync, JsonSerializationSettings

   # Work with a single file
   with JSONFile("settings.json", default_data={"theme": "dark"}) as jf:
       jf.json["count"] = 1  # saved automatically on clean exit

   # Shared instance via pool
   jf = load("data.json", default_data={})
   jf.json["x"] = 42
   sync()  # persist all pooled files

   # Control formatting
   jf.settings = JsonSerializationSettings(indent=2, sort_keys=True, ensure_ascii=False)
   jf.save()

Why singlejson?
---------------

- Minimal API with sensible defaults
- Safe writes via ``save_atomic()``
- Robust error handling (invalid JSON recovery, clear exceptions)
- Thread-safe pooling so the same path uses one in-memory object
