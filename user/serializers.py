from datetime import datetime
from rest_framework import serializers
from user.models import User,Movie
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Movie 
		fields = ('id','popularity','director','genre','imdb_score','name','cover','User','is_deleted')
		extra_kwargs = {
			'name': {
				'required':True,
				'error_messages':{
				'required':"Please fill this field",
				}
			}
		}