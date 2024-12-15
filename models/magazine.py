from database.a import CONN,CURSOR

class Magazine:

    all = {}

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS magazines(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS magazines
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM magazines
            WHERE id == ?
        """
        magazine = CURSOR.execute(sql, (id,)).fetchone()
        return cls(magazine[1], magazine[2], magazine[0]) if magazine else None

    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2], row[0])
            cls.all.update({row[0]: magazine})
        return magazine

    @property
    def id_(self):
        return self._id
    
    @id_.setter
    def id_(self, id):
        if isinstance(id, int):
            self._id= id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not hasattr(self, "name") and isinstance(name, str) and  2 <= len(name) <= 16:
            self._name = name
            return 
        self._name = name
        sql = """
            UPDATE magazines
            SET name = ? 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id_))
        CONN.commit()

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if not hasattr(self, "_category") and isinstance(category, str) and len(category) > 0:
            self._category = category
            return
        self._category = category
        sql = """
            UPDATE magazines
            SET category = ?
            WHERE id = ? 
        """
        CURSOR.execute(sql, (self.category, self.id_))
        CONN.commit()   

    def __init__(self, name, category, id=None):
        self.name = name
        self.category = category
        self.id_ = id
        self.save()

    def save(self):
        sql = """
            INSERT INTO magazines (name, category)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()

        self.id_= CURSOR.lastrowid

        type(self).all.update({self.id_: self})

    def articles(self):
        from models.article import Article
        sql = """
            SELECT *
            FROM articles
            WHERE magazine_id = ?
        """
        articles = CURSOR.execute(sql, (self.id_,)).fetchall()
        return [Article.instance_from_db(article) for article in articles]



    def __repr__(self):
        return f'<Magazine {self.name}>'
