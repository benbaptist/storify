from storify import Storify

# This code demonstrates how to use Storify to create a simple database 
# and store/retrieve key-value pairs.

def main():
    # Initialize Storify with a custom root directory
    storify = Storify()

    # Initialize a new database
    db = storify.get_db(name="simple_db")

    # Add some key-value pairs to the database
    db["example_key"] = "example_value"
    
    # Print out the stored value
    print(f"Stored value for 'example_key': {db['example_key']}")

    db.flush()

if __name__ == "__main__":
    main()
