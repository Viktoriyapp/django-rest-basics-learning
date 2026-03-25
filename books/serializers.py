from rest_framework import serializers

from books.models import Book, Publisher, Author, Review


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
    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.book = validated_data.get('book', instance.book)
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