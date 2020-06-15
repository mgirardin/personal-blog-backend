from google.cloud import firestore
from datetime import datetime
client = firestore.Client()

class Article:
    @staticmethod
    def create(post, author, metadata):
        try:
            kind = 'articles'
            doc = client.collection(kind).document()
            doc.set({
                'title': post["title"],
                'subtitle': post["subtitle"],
                'body': post["body"],
                'main_image': post["main_image"],
                'author': author["name"],
                'author_picture': author["picture"],
                'category': metadata["category"],
                'tags': metadata["tags"],
                'time_to_read': metadata["time_to_read"],
                'comments': [],
                'created_on': datetime.now(),
                'views': 0
            })
        except Exception as e:
            print(e)

    @staticmethod
    def get(id):
        try:
            kind = 'articles'
            doc_ref = client.collection(kind).document(id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def get_all():
        kind = 'articles'
        collection = client.collection(kind)
        articles = []
        for doc in collection.stream():
            articles.append(doc.to_dict())
        return articles

class User:
    @staticmethod
    def get(login):
        kind = 'users'
        query_ref = client.collection(kind).where("login", "==", login).limit(1)
        for doc in query_ref.stream():
            user = doc.to_dict()
        return user