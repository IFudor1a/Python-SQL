import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

def database_creation():
    tables = ["CREATE TABLE IF NOT EXISTS Author(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);",
              """CREATE TABLE IF NOT EXISTS Book(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);""",
              """CREATE TABLE IF NOT EXISTS Library(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              genre_type TEXT NOT NULL,
                                              author_id INTEGER NOT NULL,
                                              book_id INTEGER NOT NULL,
                                              FOREIGN KEY (author_id)
                                              REFERENCES Author ON UPDATE CASCADE ON DELETE CASCADE,
                                              FOREIGN KEY (book_id)
                                              REFERENCES Book ON UPDATE CASCADE ON DELETE CASCADE);"""
              ]

    # executing table creation
    [db.cursor.execute(i) for i in tables]

    # commiting creation of tables
    db.conn.commit()

    # data to fill up the Author table
    authors = [("Mukhtar Auezov",),
               ("Viktor Hugo",),
               ("E.M Renark",),
               ("Aleksandr Duma",)
               ]

    # data to fill up the Book table
    books = [("The Abai Way",),
             ("The Hunchback of Notre Dame",),
             ("The Arc of Triumph",),
             ("The Count of Monte Cristo",)
             ]

    # data to fill up the Library table
    library = [("histrical", "1", "1"),
               ("romanance", "2", "2"),
               ("war novel", "3", "3")
               ]

    # running the sql statments for population of tables
    db.cursor.executemany("INSERT INTO Author(name) VALUES(?)", authors)
    db.cursor.executemany("INSERT INTO Book(name) VALUES(?)", books)
    db.cursor.executemany("INSERT INTO Library(genre_type, author_id, book_id) VALUES(?,?,?)",
                       library)

    # commiting changes to db
    db.conn.commit()

def get_book_info_by_book_name(book_name):
    db.cursor.execute(f"Select id FROM Book WHERE name = '{book_name}'")
    book_id = db.cursor.fetchone()[0]
    db.cursor.execute(f"SELECT author_id FROM Library WHERE book_id = '{book_id}'")
    author_id = db.cursor.fetchone()[0]
    db.cursor.execute(f"SELECT name FROM Author WHERE id = '{author_id}'")
    author_name = db.cursor.fetchone()[0]
    print(f"author - {author_name}, book - {book_name}")
    control()

def get_available_genres():
    db.cursor.execute("SELECT genre_type FROM Library")
    print(db.cursor.fetchall())
    control()

def add_book_by_author_id(author_id):
    db.cursor.execute(f"SELECT id FROM Author WHERE id='{author_id}' and  id not in (SELECT author_id FROM Library)")
    result = db.cursor.fetchone()
    if result is None:
        genre_type = input("genre_type")
        book_name = input("book_name")
        db.cursor.execute(f"INSERT INTO Book(name) VALUES ('{book_name}')")
        db.conn.commit()

        db.cursor.execute(f"SELECT id FROM Book WHERE name = '{book_name}'")
        book_id = db.cursor.fetchone()[0]

        db.cursor.execute(f"INSERT INTO Library(genre_type, author_id, book_id) VALUES ('{genre_type}','{author_id}','{book_id}')")
        db.conn.commit()
        control()
    else:
        add_new_book_library()

def add_new_book_library():
    author_name = input("Enter author name:")
    genre_type = input("Enter genre type:")
    book_name = input("Enter book name:")
    db.cursor.execute(f"INSERT INTO Author(name) VALUES ('{author_name}')")
    db.conn.commit()
    db.cursor.execute(f"SELECT id FROM Author WHERE name = '{author_name}'")
    author_id = db.cursor.fetchone()[0]
    db.cursor.execute(f"INSERT INTO Book(name) VALUES ('{book_name}')")
    db.conn.commit()
    db.cursor.execute(f"SELECT id FROM Book Where name = '{book_name}'")
    book_id = db.cursor.fetchone()[0]

    db.cursor.execute(f"INSERT INTO Library(genre_type, author_id, book_id) VALUES ('{genre_type}','{author_id}','{book_id}')")
    db.conn.commit()
    control()

def delete_book_by_book_id(book_id):
    db.cursor.execute(f"DELETE FROM Library WHERE book_id = '{book_id}'")
    db.conn.commit()
    control()

def see_all_library_entries():
    db.cursor.execute(f"SELECT Library.genre_type, Author.name FROM Library JOIN Author ON Library.author_id = Author.id")
    result = db.cursor.fetchall()
    db.cursor.execute(f"SELECT Book.name FROM Library JOIN Book ON Library.book_id = Book.id")
    book = db.cursor.fetchall()
    for i,res in enumerate(result):
        genre_type,author_name = res
        book_name = book[i][0]
        print(f"genre - {genre_type},author - {author_name}, book - {book_name}")
    control()

def find_author_without_entry_in_library():
    db.cursor.execute(f"SELECT name FROM Author WHERE id not in (SELECT author_id FROM Library)")
    author = db.cursor.fetchall()
    db.cursor.execute(f"SELECT name FROM BOOK  WHERE id not in (SELECT book_id FROM Library) ")
    book = db.cursor.fetchall()
    for i,res in enumerate(author):
        author_name = res
        book_name = book[i][0]
        print(f"author - {author_name[0]}, book - {book_name}")
    control()
def control():
    print("1.get book info by book name\n2.get all available genres in library\n3.add book by author id\n4.add a new book to the library\n5.delete book by book_id from library\n6. see all library entries\n7.find author without entry in library\n8.exit ")
    user_input = input("choice:")
    if user_input == "1":
        book_name = input("Enter book name:")
        get_book_info_by_book_name(book_name)
    elif user_input == "2":
        get_available_genres()
    elif user_input == "3":
        author_id = input("Enter author id")
        add_book_by_author_id(author_id)
    elif user_input == "4":
        add_new_book_library()
    elif user_input == "5":
        book_id = input("Enter book id:")
        delete_book_by_book_id(book_id)
    elif user_input == "6":
        see_all_library_entries()
    elif user_input == "7":
        find_author_without_entry_in_library()
    else:
        exit()

if __name__ == "__main__":
    db = Database()
    db.connect()
    database_creation()
    control()