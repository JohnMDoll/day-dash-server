from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from daydashapi.models import DashUser

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''Handles the authentication of a player

    Method arguments:
        request -- The full HTTP request object
    '''
    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=request.data['email'], password=request.data['password'])

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        dasher = DashUser.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'firstName': authenticated_user.first_name,
            'id': dasher.id,
            'zipcode': dasher.zipcode,
            'token': token.key
            }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''Handles the creation of a new player for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        User.objects.get(email=request.data['email'])
        data = {'message': 'This email is already in use'}
    except User.DoesNotExist:

        new_user = User.objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email'],
            first_name=request.data['firstName'],
            last_name=request.data['lastName']
        )

        new_dash_user = DashUser.objects.create(
            zipcode=request.data['zipcode'],
            user=new_user
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        # this is where we update what gets sent back to the client for localStorage
        data = {
            'valid': True,
            'firstName': new_user.first_name,
            'id': new_dash_user['id'],
            'zipcode': new_dash_user.zipcode,
            'token': token.key
            }
    return Response(data)
