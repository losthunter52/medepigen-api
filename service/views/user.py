from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from common.utils import check_required_fields
from django.contrib.auth.models import User, Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not check_required_fields(data, ['username', 'password']):
        return Response({"error": "Username and password are required."}, status=400)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid username or password."}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    role = ''

    if user.groups.filter(name='admin').exists():
        role = 'admin'
    elif user.groups.filter(name='user').exists():
        role = 'user'

    response_data = {
        "token": token.key,
        "full_name": user.get_full_name(),
        "first_name": user.first_name,
        "email": user.email,
        "username": user.username,
        "role": role
    }

    return Response(response_data, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_users(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)
    
    users = User.objects.all()
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'email': user.email,
            'roles': [group.name for group in user.groups.all()]
        }
        users_data.append(user_data)

    return Response(users_data, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_user(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data
    
    required_fields = [
        'username', 
        'password',
        'first_name',
        'last_name',
        'email',
        'roles'
    ]

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)

    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    roles = data.get('roles') 
    
    for role in roles:
        if not Group.objects.filter(name=role).exists():
            return Response({"error": "Role not found."}, status=400)
    
    username_validator = UnicodeUsernameValidator()
    if len(username) > 150:
        return Response({"error": f"Invalid username."}, status=400)
    try:
        username_validator(username)
    except ValidationError as e:
        return Response({"error": "Invalid username."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    for role in roles:
        group = Group.objects.filter(name=role).first()
        user.groups.add(group)

    return Response({"message": "User creation success."}, status=201)

@api_view(['PUT'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request, username):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    
    if user.is_staff:
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    data = request.data

    required_fields = [
        'first_name',
        'last_name',
        'email',
        'roles'
    ]

    if not check_required_fields(data, required_fields):
        return Response({"error": "Missing required fields."}, status=400)
    
    new_first_name = data.get('first_name')
    new_last_name = data.get('last_name')
    new_email = data.get('email')

    new_roles = data.get('roles')

    for role in new_roles:
        if not Group.objects.filter(name=role).exists():
            return Response({"error": "Role not found."}, status=400)

    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email
    
    user.groups.clear()
    for role in new_roles:
        group = Group.objects.filter(name=role).first()
        user.groups.add(group)

    if 'username' in data:
        new_username = data.get('username')
        username_validator = UnicodeUsernameValidator()
        if len(new_username) > 150:
            return Response({"error": f"Invalid username."}, status=400)
        try:
            username_validator(new_username)
        except ValidationError as e:
            return Response({"error": "Invalid username."}, status=400)

        if User.objects.filter(username=new_username).exists():
            return Response({"error": "Username already exists."}, status=400)
        user.username = new_username

    if 'password' in data:
        user.set_password(data['password'])

    user.save()
    return Response({"message": "User updated successfully."}, status=200)

@api_view(['DELETE'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, username):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    
    if request.user.username == user.username:
        return Response({"error": "Cannot delete own user."}, status=400)
    
    if user.is_staff:
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    user.delete()
    return Response({"message": "User deleted successfully."}, status=200)

@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def clone_user(request):

    if not request.user.groups.filter(name='admin').exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    original_username = request.data.get('username')

    try:
        original_user = User.objects.get(username=original_username)
    except User.DoesNotExist:
        return Response({"error": "Original user not found."}, status=404)

    new_username = f"{original_user.username}_clone"

    while User.objects.filter(username=new_username).exists():
        new_username += "_clone"

    username_validator = UnicodeUsernameValidator()

    if len(new_username) > 150:
        return Response({"error": f"Invalid username."}, status=400)
    try:
        username_validator(new_username)
    except ValidationError as e:
        return Response({"error": f"Invalid username."}, status=400)

    cloned_user = User.objects.create_user(
        username=new_username,
        password=original_user.password, 
        first_name=original_user.first_name,
        last_name=original_user.last_name,
        email=original_user.email
    )

    original_groups = original_user.groups.all()
    for group in original_groups:
        cloned_user.groups.add(group)

    return Response({"message": "User cloning success."}, status=201)
