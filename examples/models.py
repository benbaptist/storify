from storify import Storify
from storify.model import Model

class Book(Model):
    def __init__(self) -> None:
        self.title = ""
        self.author = ""
        self.year = 0
        
def main():
    # Initialize Storify with a custom root directory
    storify = Storify(models=[Book])

    # Initialize a new database
    db = storify.get_db(name="books_db")

    # Add a list to the database, if it doesn't already exist
    if "books" not in db:
        db["books"] = []

    # Create some book instances
    book1 = Book()
    book1.title = "1984"
    book1.author = "George Orwell"
    book1.year = 1949

    book2 = Book()
    book2.title = "To Kill a Mockingbird"
    book2.author = "Harper Lee"
    book2.year = 1960

    book3 = Book()
    book3.title = "The Great Gatsby"
    book3.author = "F. Scott Fitzgerald"
    book3.year = 1925

    books_to_add = [book1, book2, book3]

    # Store books in the database
    for book in books_to_add:
        db["books"].append(book)

    # Print out all books in our database, including ones from previous runs of this script
    for book in db["books"]:
        print(f"'{book.title}' by {book.author}, published in {book.year}")

    # Flush all databases (force save)
    storify.flush()

if __name__ == "__main__":
    main()
