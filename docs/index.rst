.. storify documentation master file, created by
   sphinx-quickstart on Sat Jul 27 11:00:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Storify's documentation!
===================================

Storify is a dead-simple, lightweight Python database library that uses msgpack for efficient data serialization.

It provides a framework for data storage and retrieval, with an optional ORM model for interaction with data.

Storify supports automatic backups and error handling, ensuring data integrity and reliability.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api/index
   contributing
   license

Features
--------

- Create and manage multiple msgpack-based databases with ease.
- Lightweight ORM-esque model for easy interaction with data.
- Automatic backups and data flushing to prevent data loss.
- Built-in error handling to automatically recover from database corruption and loading issues.
- Configurable save intervals for optimized performance.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 