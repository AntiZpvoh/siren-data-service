from rest_framework import serializers
from v1.models import User
class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = User
      fields = "__all__"