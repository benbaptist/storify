from storify import Storify

# This code demonstrates how to use Storify to create a simple database 
# outside of the Storify root directory.

def main():
    # Initialize Storify with a custom root directory
    storify = Storify()

    # Initialize a new database
    db = storify.get_db_by_path("example_data/super_simple_db.mpack")

    # Add some key-value pairs to the database
    db["example_key"] = "example_value"
    
    # Print out the stored value
    print(f"Stored value for 'example_key': {db['example_key']}")

    db.flush()

if __name__ == "__main__":
    main()
