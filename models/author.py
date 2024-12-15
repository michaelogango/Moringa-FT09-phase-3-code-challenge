from database.connection import get_db_connection
class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        
        if len(name) == 0 or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (id, name) VALUES (?, ?)", (self._id, self._name))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE author_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            INNER JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines