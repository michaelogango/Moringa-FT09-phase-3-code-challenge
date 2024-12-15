from database.connection import get_db_connection
class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category
        
        if not (2 <= len(name) <= 16) or not isinstance(name, str):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if len(category) == 0 or not isinstance(category, str):
            raise ValueError("Category must be a non-empty string.")
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)", (self._id, self._name, self._category))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = new_name
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET name = ? WHERE id = ?", (new_name, self._id))
        conn.commit()
        conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if len(new_category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = new_category
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET category = ? WHERE id = ?", (new_category, self._id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None
