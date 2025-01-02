from database.a import CURSOR, CONN

class Article:

    all = {}

    def __init__(self, title, content, author_id, magazine_id, id=None):
        type(self).create_table()
        self.id_ = id
        self.title = title
        self.content = content
        self.author_id = author_id.id_
        self.magazine_id = magazine_id.id_
        self.save()

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (id)
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS articles
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            article.title = row[1]
            article.content = row[2]
            article.author_id = row[3]
            article.magazine_id = row[4]
        else:
            article = cls(row[1],row[2],row[3],row[4],row[0])
            cls.all.update({row[0]: article})
        return article

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if not hasattr(self, "_title") and isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title

    def author(self):
        from models.author import Author
        sql = """
            SELECT authors.id, authors.name, articles.author_id
            FROM authors
            INNER JOIN articles
            ON authors.id = ?
        """
        author = CURSOR.execute(sql, (self.author_id,)).fetchone()
        return Author(author[1], author[0])
    
    def magazine(self):
        from models.magazine import Magazine
        sql = """
            SELECT magazines.id, magazines.name, magazines.category, articles.magazine_id
            FROM magazines
            INNER JOIN articles
            ON magazines.id = ?
        """
        magazine = CURSOR.execute(sql, (self.magazine_id,)).fetchone()
        return Magazine(magazine[1], magazine[2], magazine[0])

    def save(self):
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id ))
        CONN.commit()

        self.id_ = CURSOR.lastrowid
        type(self).all.update({self.id_ : self})

    def __repr__(self):
        return f'<Article {self.title}>'
