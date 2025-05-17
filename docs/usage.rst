Usage
=====

Here's a simplified example of how to use the `storify` package:

.. code-block:: python

   from storify import Storify

   # Initialize Storify
   storify = Storify(root="example_data")
   db_name = "example_db"

   # Check if the database exists
   if storify.db_exists(db_name):
       print(f"Database '{db_name}' exists. It will be loaded.")

   # Initialize a new database
   db = storify.get_db(name=db_name)

   # Add some data to the database 
   db["key1"] = "value1" 
   db["key2"] = "value2"

   # Get some data from the database
   print(f"key1: {db['key1']}")
   print(f"key2: {db['key2']}")

   # Flush all databases (force save)
   storify.flush()

For more complete examples, including how to use the ORM, please check the ``examples`` folder in the project repository. 