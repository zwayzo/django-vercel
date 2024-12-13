from rest_framework import serializers

class userSerializer(serializers.Serializer):
    # id = serializers.AutoField(primary_key=True)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)  # Django expects hashed password here