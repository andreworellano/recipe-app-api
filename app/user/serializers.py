"""
Serializers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        # min information needed (so don't worry about is active, is staff)
        # we don't uses setting that just the admins
        fields = ['email', 'password', 'name']
        # extra arguments for fields being passed in
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    # instance that's being updated
    # validated data is being passed through serializer validation
    def update(self, instance, validated_data):
        """Update and return user"""
        # pop removes the password from the dict when retrieved
        # get would just grab it and leave it in the dict
        # password isn't needed for the request hence the 'None'
        password = validated_data.pop('password', None)
        # super() calls the update on the modelserializer base class
        user = super().update(instance, validated_data)

        # true if a user specificied a password
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
