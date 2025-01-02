import ipdb
from database.a import CONN,CURSOR

class Author:

    all = {}

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS authors
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM authors 
            WHERE id == ?
        """
        author = CURSOR.execute(sql, (id,)).fetchone()
        return cls(author[1], author[0]) if author else None

    @classmethod
    def instance_from_db(cls, row):
        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1],row[0])
            cls.all.update({row[0]: author})
        return author

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, id):
        if isinstance(id, int):
            self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not hasattr(self, '_name') and isinstance(name, str) and len(name) > 0:
            self._name = name

    def __init__(self, name, id=None):
        type(self).create_table()
        self.id_ = id
        self.name = name
        self.save()

    def save(self):
        sql = """
            INSERT INTO authors (name) 
            VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))
        CONN .commit()

        self.id_ = CURSOR.lastrowid

        type(self).all.update({self.id_ : self})

    def articles(self):
        from models.article import Article
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?
        """
        articles = CURSOR.execute(sql, (self.id_,)).fetchall()
        return [Article.instance_from_db(article) for article in articles]
 
    def magazines(self):
        from models.magazine import Magazine
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM articles
            INNER JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """
        magazines = CURSOR.execute(sql, (self.id_,)).fetchall()
        return [Magazine.instance_from_db(magazine) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self.name}>'
    
