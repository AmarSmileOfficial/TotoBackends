from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from todo.models import Todo
from todo.serializers import TodoSerializer
from django.shortcuts import get_object_or_404
import logging

# Create a logger
logger = logging.getLogger(__name__)

class CreateTodo(APIView):
    def post(self, request):
        try:
            # Retrieve data from the request
            title = request.data.get('title')
            description = request.data.get('description')
            completed = request.data.get('completed', False)

            # Check if any parameter is null or empty
            if not title or not description:
                response_data = {
                    'error': 'Title and description are required fields.'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            if len(title) > 150:
                response_data = {
                    'error': 'Title is too long (maximum 150 characters).'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if len(description) > 500:
                response_data = {
                    'error': 'Description is too long (maximum 500 characters).'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # If validation passes, create the Todo item
            todo = Todo.objects.create(title=title, description=description, completed=completed)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log the exception
            logger.error(f"An error occurred: {e}")

            # Handle exceptions (e.g., database errors)
            response_data = {'error': 'An error occurred while processing the request.', 'detail': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListTodos(APIView):
    def get(self, request):
        try:
            # Get request parameters
            filter = request.data.get('filter',None)

            # Fetch and filter Todo items based on the filter parameter
            if filter == 'completed':
                todos = Todo.objects.filter(completed=True)
            elif filter == 'incomplete':
                todos = Todo.objects.filter(completed=False)
            else:
                todos = Todo.objects.all()

            # Serialize Todo items
            serializer = TodoSerializer(todos, many=True)

            # Return the serialized data as a JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception
            logger.error(f"An error occurred: {e}")

            # Handle exceptions (e.g., database errors)
            response_data = {'error': 'An error occurred while processing the request.', 'detail': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateTodo(APIView):
    def put(self, request):
        try:
            # Check if the Todo item exists
            id = request.data.get('id')
            todo = get_object_or_404(Todo, pk=id)

            # Retrieve data from the request
            title = request.data.get('title', todo.title)
            description = request.data.get('description', todo.description)
            completed = request.data.get('completed', todo.completed)

            # Check if the updated title and description are valid
            if len(title) > 150:
                response_data = {
                    'error': 'Title is too long (maximum 150 characters).'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if len(description) > 500:
                response_data = {
                    'error': 'Description is too long (maximum 500 characters).'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Update the Todo item
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.save()

            # Serialize and return the updated Todo item
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception
            logger.error(f"An error occurred: {e}")

            # Handle exceptions (e.g., database errors)
            response_data = {'error': 'An error occurred while processing the request.', 'detail': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class RetrieveTodo(APIView):
    def get(self, request):
        try:
            # Check if the Todo item exists
            id = request.data.get('id')
            todo = get_object_or_404(Todo, pk=id)

            # Serialize and return the retrieved Todo item
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)    

        except Exception as e:
            # Log the exception
            logger.error(f"An error occurred: {e}")

            # Handle exceptions (e.g., database errors)
            response_data = {'error': 'An error occurred while processing the request.', 'detail': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteTodo(APIView):
    def delete(self, request):
        try:
            # Check if the Todo item exists
            id = request.data.get('id')
            todo = get_object_or_404(Todo, pk=id)

            # Delete the Todo item
            todo.delete()

            # Return a success response
            return Response({'message': 'Todo item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            # Log the exception
            logger.error(f"An error occurred: {e}")

            # Handle exceptions (e.g., database errors)
            response_data = {'error': 'An error occurred while processing the request.', 'detail': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)