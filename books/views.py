from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from books.serializers import BookSerializer


# Create your views here.

class HomeView(APIView):
    def get(self, request):
        return HttpResponse({"text": "helloo!"}, content_type="application/json")


# class BookListCreateView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookListCreateView(APIView):
    def get(self, request: Request) -> Response:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BookDetailView(APIView):
    def get_object(self, pk: int) -> Book:
        return get_object_or_404(Book, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        book = self.get_object(pk=pk)
        serializer = BookSerializer(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response: # we edit the whole object, without missing values
        book = self.get_object(pk=pk)
        serializer = BookSerializer(book, data=request.data) # the book instance and the new data to add
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response: # can change only one thing(partial), without giving the whole object but only a part of it
        book = self.get_object(pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response: # we dont need serializer here
        book = self.get_object(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)