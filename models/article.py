from database.connection import get_db_connection
class Article:
    def __init__(self, author, magazine, title):
        self._author = author
        self._magazine = magazine
        self._title = title
        
        if not (5 <= len(title) <= 50) or not isinstance(title, str):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        # Insert into database
        conn = get_db_connection('./database/magazine.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)",
                       (self._author.id, self._magazine.id, self._title))
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine