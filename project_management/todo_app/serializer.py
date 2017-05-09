from rest_framework import serializers
from django.contrib.auth import get_user_model 
from .models import TodoDetail 
from rest_framework.fields import CurrentUserDefault
import pdb
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('id','username','password')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoDetail
        fields = ('id','user','todo', 'status',)

    def create(self, validated_data):
    	todo = TodoDetail.objects.create(
	        	user= validated_data['user'],
	            todo=validated_data['todo'],
              # tag = validated_data['tag']
	            status=validated_data.get('status',1),
	        )
        todo.save()
        return todo

  	def update(self,validated_data):
  		todo = TodoDetail.objects.get(id=validated_data['id'])
  		todo.todo = validated_data.get('todo', todo.todo )
  		todo.status = validated_data.get('status', todo.status )
  		todo.save
  		return todo
