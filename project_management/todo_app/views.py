from rest_framework import permissions
# from rest_framework.generics import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import TodoDetail, TagDetail # If used custom user model
import pdb
from .serializer import UserSerializer, TodoSerializer


class UserView(APIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def get(self, request, format=None):
		UserObj = User.objects.all()
		serializer = UserSerializer(UserObj, many=True)		
		return Response(serializer.data)	

    def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response('success', status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoView(APIView):

    model = TodoDetail
    serializer_class = TodoSerializer

    def create(self, request, format=None):
        tag_name =request.POST['tag'].split(',')
        for t in tag_name:
            tag_obj = TagDetail.objects.filter(tag=t)
            if not tag_obj:
                tag_create_obj = TagDetail.objects.create(tag=t)
                tag_create_obj.save()
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            todo_obj = serializer.save()
            todo_obj['tag'] = TagDetail.objects.filter(tag=t)
            todo_obj.save()
            return Response('success', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, format=None):
    	if not request.GET.get('id'):
    		return Response("Required ID", status=status.HTTP_400_BAD_REQUEST)
    	todo = TodoDetail.objects.filter(id=request.GET['id'])
    	if not todo:
    		return Response("Not a valid ID", status=status.HTTP_400_BAD_REQUEST)
    	else:
    		todo=todo[0]
    	todo.delete()
    	return Response('deleted', status=status.HTTP_201_CREATED)
    
    def put(self,request, format=None):
    	request.__mutable = True
    	if not request.GET.get('id'):
    		return Response("Required ID", status=status.HTTP_400_BAD_REQUEST)
    	pdb.set_trace()
    	request.data.update({'user':request.user.id})
    	serializer = TodoSerializer(data=request.data)
    	if serializer.is_valid():
    		todo = TodoDetail.objects.filter(id=request.GET['id'])
    		if not todo:
    			return Response("Not a valid ID", status=status.HTTP_400_BAD_REQUEST)
    		else:
    			todo=todo[0]
    		for f in request.data.keys():
    			if not f=='user':
					todo.__setattr__(f,request.data.get(f))
    		todo.save()
    		return Response('updated', status=status.HTTP_201_CREATED)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
    	# update user object
    	request.__mutable = True
    	request.data.update({'user':request.user.id})
    	serializer = TodoSerializer(data=request.data)
    	if serializer.is_valid():
    		serializer.save()
    		return Response('success', status=status.HTTP_201_CREATED)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
		TodoObj = TodoDetail.objects.filter(user=request.user.id)
		serializer = TodoSerializer(TodoObj, many=True)		
		return Response(serializer.data)

	