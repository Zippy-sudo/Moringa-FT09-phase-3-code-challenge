import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        author = Author("Whomsoever")
        magazine = Magazine("Whiplash", "Movie")
        article = Article("Test Title", "Test Content", author, magazine, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
