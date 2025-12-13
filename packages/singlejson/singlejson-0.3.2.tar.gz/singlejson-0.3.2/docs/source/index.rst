.. singlejson documentation master file, created by
   sphinx-quickstart on Mon May 20 19:39:32 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to singlejson's documentation!
======================================

Singlejson is a tiny helper to load and save JSON files as shared objects
across your codebase. It offers a friendly `JSONFile` wrapper, a thread‑safe
pool for shared instances, and configurable serialization.

Installation & basic usage
====================================
Install with pip:

.. code-block:: bash
    :substitutions:

   pip install singlejson==|release|

Here is a quick example to get you started:

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


Get started in a minute using the guide below, or dive into the API reference.

.. toctree::
   :maxdepth: 2
   :caption: Guide

   getting_started
   advanced

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`