# Storify API Developer Guide

## 1. Introduction

Storify is a Python library designed to provide a simple and an easy-to-use interface for file-based data storage. It uses MessagePack (`msgpack`) for efficient serialization and deserialization of data, and supports defining custom data models. Each database is essentially a persistent dictionary-like object, making it intuitive to store and retrieve Python objects.

Key features include:
-   **Simple API**: Easy to get started with managing and interacting with databases.
-   **File-Based**: Data is stored in local files, making it portable.
-   **Msgpack Serialization**: Efficient binary serialization for speed and space.
-   **Custom Models**: Define your own classes that can be automatically serialized and deserialized.
-   **Automatic Backups**: Built-in mechanism for backing up databases before flushing changes.
-   **Data Integrity**: Attempts to recover from corrupted database files using backups.

This guide provides API developers with the information needed to utilize the `storify` module effectively.

## 2. Installation

Install using pip:
```bash
pip install storify
```

## 3. Core Concepts

### 3.1. `Storify`
The `Storify` class (from `storify/__init__.py`) is the main entry point and acts as a manager for multiple database instances. It handles:
-   The root directory where all managed database files are stored.
-   Retrieval or creation of `Database` instances.
-   Periodic saving (ticking) of all managed databases.

### 3.2. `Database`
The `Database` class (from `storify.database/__init__.py`) represents a single data store.
-   Its data is primarily dictionary-like, allowing key-value storage.
-   It handles the serialization (`msgpack.packb`) and deserialization (`msgpack.unpackb`) of its contents to/from a `.mpack` file.
-   It supports automatic loading from disk and saving (flushing) changes.
-   It manages its own backups.
-   Can automatically handle instances of custom `Model` classes if they are registered.

### 3.3. `Model`
The `Model` class (from `storify.model.py`) is a base class that developers can inherit from to create their own custom data structures.
-   Objects of classes inheriting from `Model` can be stored in a `Database` and will be automatically serialized and deserialized.
-   Key methods for serialization control:
    -   `_to_dict()`: Converts the model instance to a dictionary for serialization.
    -   `_from_dict(data)`: Populates a model instance from a dictionary during deserialization.
    -   `_keyname()`: (Class method) Returns a unique string key used to identify the model type during serialization. Defaults to `__ClassName__`.

## 4. Getting Started

### 4.1. Initializing `Storify`

First, import and initialize the `Storify` class.

```python
from storify import Storify

# Initialize Storify, specifying the root directory for databases
# and an auto-save interval (in seconds).
sf = Storify(root="my_app_data", save_interval=300) # Auto-saves every 5 minutes

# You can also provide a custom logger and register model classes
# from my_models import User, Product
# sf = Storify(root="my_app_data", models=[User, Product], verbose=True)
```

### 4.2. Getting/Creating a `Database`

Use the `get_db()` method of your `Storify` instance to obtain a database. If the database file doesn't exist, it will be created.

```python
# Get (or create if it doesn't exist) a database named 'users'
user_db = sf.get_db("users")

# If creating a new database, you can provide an initial root data structure
# (defaults to an empty dictionary {})
# product_db = sf.get_db("products", root={"items": [], "categories": {}})

# You can also access databases using dictionary-like syntax
# user_db = sf["users"]
```

## 5. Working with Databases

A `Database` object behaves much like a Python dictionary.

### 5.1. Basic CRUD Operations

```python
# Assuming user_db = sf.get_db("users")

# Create / Update
user_db["user123"] = {"name": "Alice", "email": "alice@example.com"}
user_db["user456"] = {"name": "Bob", "age": 30}

# Read
alice_data = user_db["user123"]
print(alice_data) # Output: {'name': 'Alice', 'email': 'alice@example.com'}

# Check for existence
if "user789" in user_db:
    print("User 789 exists.")
else:
    print("User 789 does not exist.")

# Delete
if "user456" in user_db:
    del user_db["user456"]

# Iterate over keys
for user_id in user_db:
    print(f"User ID: {user_id}, Data: {user_db[user_id]}")

# Get number of top-level items
num_users = len(user_db)
print(f"Total users: {num_users}")
```
The `Database` class also has `append`, `remove`, and `pop` methods, suggesting its internal `self.data` can be a list. However, typical usage shown is dictionary-like. Ensure the structure of `db.data` matches the methods you use.

### 5.2. Saving Data (`flush`, `tick`)
-   **Automatic Saving**: The `Storify` instance periodically calls `tick()` on all its managed databases based on the `save_interval` provided during initialization. `tick()` will call `db.flush()` if enough time has passed since the last flush.
-   **Manual Saving**:
    -   `db.flush()`: Call this on a `Database` instance to immediately save its current state to disk. This also creates a backup.
    -   `sf.flush()`: Call this on a `Storify` instance to force an immediate flush of all active databases it manages.

```python
# Manually save a specific database
user_db.flush()

# Manually save all databases managed by Storify
sf.flush()
```

### 5.3. Loading Data
Data is loaded automatically when a `Database` instance is created (via `sf.get_db()` or by directly instantiating `Database`) if its corresponding `.mpack` file exists. The `db.load()` method handles this, including attempts to restore from backups if the main file is corrupted.

### 5.4. Closing and Destroying Databases
-   `db.close()`: Flushes the database to disk and marks it as defunct (unusable). The data file remains.
-   `db.destroy()`: Closes the database and then deletes its `.mpack` file from disk. Backups are preserved.

```python
# Close the database (saves data, file remains)
# user_db.close()

# Destroy the database (saves data, then deletes file)
# user_db.destroy() # After this, user_db instance should not be used.
```

### 5.5. Managing Databases (via `Storify` instance)
-   `sf.db_exists(name)`: Checks if a database file exists in the `Storify` root directory.
-   `sf.rename_db(old_name, new_name)`: Renames a database file. **Warning**: Dangerous to use if the database is currently open.
-   `sf.remove_db(name)`: Removes a database file. This is equivalent to `sf[name].destroy()` but acts directly on the file system. **Warning**: May be ineffective if the database is currently open by an active `Database` instance. It's safer to get the DB instance and call `.destroy()`.

```python
if sf.db_exists("old_users_db"):
    sf.rename_db("old_users_db", "archived_users_db")

# To safely remove a database:
# if sf.db_exists("temp_db"):
#     temp_db = sf.get_db("temp_db")
#     temp_db.destroy() # This calls close() then removes the file
# Alternatively, but with caution:
# sf.remove_db("temp_db")
```

## 6. Using Models

You can define custom classes that inherit from `storify.Model` to have their instances automatically serialized and deserialized by the `Database`.

### 6.1. Defining a Custom Model

```python
from storify.model import Model

class User(Model):
    def __init__(self, user_id=None, name=None, email=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        # Attributes starting with '_' are not serialized by default _to_dict
        self._session_token = None 

    def __repr__(self):
        return f"<User(id={self.user_id}, name='{self.name}')>"

    # _to_dict() and _from_dict(data) are inherited from Model.
    # Override them if you need custom serialization logic.

    # _keyname() is inherited. It will return "__User__" by default.
    # Override if you need a different key (e.g., for versioning or namespacing)
    # @classmethod
    # def _keyname(cls):
    #     return "v1_user_model"

class Product(Model):
    def __init__(self, product_id=None, name=None, price=0.0):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.name}', price={self.price})>"
```

### 6.2. Registering Models
For the `Database` to automatically recognize and handle your custom models during deserialization, you need to pass a list of your model classes to the `Storify` instance or directly to a `Database` instance.

```python
from storify import Storify
# from my_app.models import User, Product # Assuming models are in this file

# Register models with Storify instance
sf = Storify(root="app_data", models=[User, Product])

# Get a database; it will now be aware of User and Product models
data_db = sf.get_db("my_data")

# --- Storing and retrieving model instances ---
alice = User(user_id="u001", name="Alice Wonderland", email="alice@wonder.land")
potion = Product(product_id="p001", name="Shrinking Potion", price=10.99)

data_db["alice_profile"] = alice
data_db["potion_item"] = potion

# Important: The database needs to be flushed/saved for changes to persist
data_db.flush()

# Later, or in another session:
sf_reloaded = Storify(root="app_data", models=[User, Product])
data_db_reloaded = sf_reloaded.get_db("my_data")

retrieved_alice = data_db_reloaded["alice_profile"]
retrieved_potion = data_db_reloaded["potion_item"]

print(retrieved_alice) # Output: <User(id=u001, name='Alice Wonderland')>
print(isinstance(retrieved_alice, User)) # Output: True

print(retrieved_potion) # Output: <Product(id=p001, name='Shrinking Potion', price=10.99)>
print(isinstance(retrieved_potion, Product)) # Output: True
```

When a `Model` instance is stored, `_to_dict()` is called, and the result is wrapped with its `_keyname()`: `{"__User__": {"user_id": "u001", ...}}`.
When data is loaded, if a dictionary matches this pattern, `_deserialize()` (which calls `_from_dict()`) on the corresponding registered model class is used to recreate the object.

## 7. Error Handling

The primary custom exception you might encounter is:
-   `storify.exceptions.DatabaseLoadError`: Raised if a database file cannot be loaded from its primary path or any of its backups. This usually indicates file corruption that couldn't be automatically resolved.

```python
from storify import Storify
from storify.exceptions import DatabaseLoadError

sf = Storify(root="data_dir")
try:
    # Potentially problematic if 'corrupt_db.mpack' is badly corrupted
    db = sf.get_db("corrupt_db") 
except DatabaseLoadError as e:
    print(f"Failed to load database: {e}")
    # Implement recovery logic, e.g., initialize with empty data or notify admin
    # db = sf.get_db("corrupt_db", root={}) # Recreate as empty
```

Other errors might be standard Python exceptions like `IOError` (e.g., disk full during `flush`) or `KeyError` (accessing non-existent keys).

## 8. Logging

Storify uses a custom `Logger` class (in `storify.logger`) which is a simple wrapper around Python's standard `logging` module.
-   When you initialize `Storify`, you can pass your own logger instance: `sf = Storify(log=my_custom_logger)`.
-   If no logger is provided, a default `Logger` is created.
-   You can set `verbose=True` when initializing `Storify` to set the default logger level to `DEBUG` (otherwise `INFO`).

```python
import logging
from storify import Storify
from storify.logger import Logger # To create a Storify compatible logger

# Using Python's logging
my_logger = logging.getLogger("MyApplication")
my_logger.setLevel(logging.DEBUG)
# ... configure handlers for my_logger ...

# Pass a compatible logger (it needs info, debug, error, warning, traceback methods)
# Storify's Logger class instance is compatible. For standard library loggers,
# you might need a small wrapper if Storify's internal calls expect exactly
# the 'Logger' class API (e.g. specific `traceback` method signature).
# However, Storify's Logger itself uses a standard library logger, so it should be fine.

class MyCustomStorifyLogger: # Adheres to Storify's Logger interface
    def __init__(self, logger_instance):
        self._logger = logger_instance
    def info(self, msg): self._logger.info(msg)
    def debug(self, msg): self._logger.debug(msg)
    def error(self, msg): self._logger.error(msg)
    def warning(self, msg): self._logger.warning(msg)
    def traceback(self, msg): self._logger.error(msg, exc_info=True)


custom_log_wrapper = MyCustomStorifyLogger(my_logger)
sf = Storify(root="app_data", log=custom_log_wrapper)
```

## 9. Advanced Topics

### 9.1. Direct Database Access by Path
If you need to work with a Storify database file that is not managed under a `Storify` root directory, you can use `Storify.get_db_by_path()` or instantiate `Database` directly with a `path`:

```python
from storify import Storify, Database
# from my_app.models import User # Assuming User model

# Using Storify helper (preferred if you have a Storify instance for config like models)
sf_config_source = Storify(models=[User]) # Use for models list, logger etc.
db_direct1 = sf_config_source.get_db_by_path("/path/to/my/external_db.mpack")

# Or instantiating Database directly
# db_direct2 = Database(path="/path/to/my/other_db.mpack", models=[User])

db_direct1["some_key"] = "some_value"
db_direct1.flush()
```
Note that such databases are not managed by any `Storify` instance's auto-save `tick()` mechanism unless you manually add them to a `Storify` instance's `databases` list and manage their lifecycle.

### 9.2. Backup Mechanism
Storify includes an automatic backup system (handled by `storify.database.backups.Backups`).
-   Before a `Database` is flushed (saved), its existing file is backed up into a subdirectory (e.g., `data/.backups/your_db_name/`).
-   Backups are timestamped.
-   If `db.load()` fails to read the main database file, it automatically attempts to load from the latest valid backup.
-   The number of backups kept might be configurable (check `Backups` class or related settings if available, not detailed in current context).

This is mostly transparent to the user but provides a safety net against data corruption.

## 10. Full Example

Here's a small example demonstrating some of the key features:

```python
import os
import shutil
from storify import Storify
from storify.model import Model

# --- 1. Define Models ---
class Task(Model):
    def __init__(self, task_id=None, description=None, completed=False):
        self.task_id = task_id
        self.description = description
        self.completed = completed

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"<Task {status} ({self.task_id}): {self.description}>"

    # Using default _keyname() == "__Task__"
    # Using default _to_dict() and _from_dict()

# --- 2. Setup Storify ---
DATA_ROOT = "todo_app_data"
# Clean up previous run for example's sake
if os.path.exists(DATA_ROOT):
    shutil.rmtree(DATA_ROOT)

sf = Storify(root=DATA_ROOT, models=[Task], verbose=True, save_interval=10) # Short interval for demo
print(f"Storify initialized. Data will be stored in: {os.path.abspath(DATA_ROOT)}")

# --- 3. Get a Database ---
todo_db = sf.get_db("daily_tasks")
print(f"Database 'daily_tasks' loaded/created at: {todo_db.path}")

# --- 4. Add Data (Model Instances) ---
task1 = Task(task_id="t1", description="Buy groceries")
task2 = Task(task_id="t2", description="Read Storify docs", completed=True)
task3 = Task(task_id="t3", description="Write example code")

todo_db[task1.task_id] = task1
todo_db[task2.task_id] = task2
todo_db["some_other_data"] = {"info": "This is not a Task object"} # Store plain dicts too

# --- 5. Add more data and use direct attribute access for models ---
todo_db[task3.task_id] = task3
current_task3 = todo_db[task3.task_id]
if isinstance(current_task3, Task):
    current_task3.description = "Write an awesome example code for Storify"
    # The change to current_task3 is a change to the object in todo_db.data
else:
    print("Error: t3 is not a Task object after retrieval!")


# --- 6. Print current DB state (in-memory) ---
print("\n--- Current DB State (in-memory) ---")
for key, value in todo_db.data.items(): # Access .data directly for full view
    print(f"{key}: {value}")

# --- 7. Flush data to disk ---
print("\nFlushing database to disk...")
todo_db.flush() # Manually flush, this will also trigger a backup
print(f"Database flushed. Check '{todo_db.path}' and its backups.")

# --- 8. Simulate application restart: Load data again ---
print("\n--- Simulating App Restart ---")
sf_reloaded = Storify(root=DATA_ROOT, models=[Task], verbose=True)
todo_db_reloaded = sf_reloaded.get_db("daily_tasks")

print("\n--- Reloaded DB State ---")
for key, value in todo_db_reloaded.data.items():
    print(f"{key}: {value}")
    if isinstance(value, Task):
        print(f"  Task ID: {value.task_id}, Completed: {value.completed}")

# --- 9. Modify data and rely on Storify's tick for saving (or manual flush) ---
retrieved_task1 = todo_db_reloaded.get("t1")
if retrieved_task1:
    retrieved_task1.completed = True
    print(f"\nMarked '{retrieved_task1.description}' as completed.")

# sf_reloaded.flush() # Or wait for save_interval

print("\n--- Final State (after modification) ---")
for key, value in todo_db_reloaded.data.items():
    print(f"{key}: {value}")

# --- 10. Clean up (optional) ---
# print(f"\nTo clean up, delete the directory: {DATA_ROOT}")
# shutil.rmtree(DATA_ROOT)

```

This guide should provide a comprehensive overview for developers looking to use the Storify module.
Make sure to replace `<repository_url>` with the actual URL if you intend to share this.
The example `my_app.models` is a placeholder; adjust paths as necessary. 