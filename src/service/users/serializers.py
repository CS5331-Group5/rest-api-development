from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import User
from diary.models import Diary

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'password', 'age')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
	    fullname=validated_data['fullname'],
            age=validated_data['age'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user
