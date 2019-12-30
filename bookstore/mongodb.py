import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=client.bookstore


stock
{
    "tags": List,
    "pictures": List,
    "id": String,
    "title": String,
    "author": String,
    "publisher": String,
    "original_title": String,
    "translator": String,
    "pub_year": String,
    "pages": int,
    "price": int,
    "binding": String,
    "isbn": String,
    "author_intro": String,
    "book_intro": String,
    "content": String
    "owner": List
}