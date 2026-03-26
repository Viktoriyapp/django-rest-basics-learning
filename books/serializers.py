from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Book, Publisher, Author, Review


UserModel = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        """
        {
            "name": "viki",
            "books": [
                1,
                2,
                3,
            ]
        }

        books = BookSerializer(many=True, read_only=True) ->
        {
            "name": "viki",
            "books": [
                {
                    "title": "Book 1",
                    "decsription": "..."
                },
                {...},
                {...},
            ]
        }
        """


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer() # serializer field
    """
    Означава че полето book в този serializer ще се обработва чрез друг serializer (BookSerializer)
    book е поле, което се валидира и сериализира чрез BookSerializer
    “Очаквам book да е обект (dict), не просто ID”
    -> Ако го нямаме DRF ще очаква: 
        {
            "book": 1
        }
    само ID (ForeignKey)
    """

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        book_data = validated_data.pop('book') # {title: Book name, ... }
        authors_data = book_data.pop('authors', [])

        book = Book.objects.create(**book_data)
        if authors_data:
            book.authors.set(authors_data)

        return Review.objects.create(book=book, **validated_data)

    def update(self, instance, validated_data):
        book_data = validated_data.pop('book', None) # dict

        instance.description = validated_data.get('description', instance.description)

        if book_data:
            authors_data = book_data.pop('authors', None)

            for attr, value in book_data.items(): # ("title", "Book name")
                setattr(instance.book, attr, value) # What we do here: instance.book.title = value

            if authors_data:
                instance.book.authors.set(authors_data)
            instance.book.save()

        instance.save()
        return instance


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(
#         max_length=200,
#     )
#     pages = serializers.IntegerField(
#         default=0,
#     )
#     description = serializers.CharField(
#         max_length=100,
#         default="",
#     )
#     author = serializers.CharField(
#         max_length=100,
#     )
#
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.pages = validated_data.get('pages', instance.pages)
#         instance.description = validated_data.get('description', instance.description)
#         instance.author = validated_data.get('author', instance.author)
#         instance.save()
#         return instance