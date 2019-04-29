from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status, exceptions
from django.contrib.auth.models import User
import jwt, json
from django.contrib.auth import authenticate
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from .models import Contact, UserContactMapping, UserProfile
from .serializers import ContactSerializer


class ContactsList(APIView):

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        auth = TokenAuthentication()
        user, error = auth.authenticate(request)
        if (error):
            return Response(
                error,
                status=400,
                content_type="application/json"
            )
        else:
            name = request.data.get('name', None)
            email = request.data.get('email', None)
            phone = request.data.get('phone', None)
            contact = Contact(
                name=name,
                phone=phone,
                email=email
            )
            contact.save()

            # mapping the contact to the user who saved it
            mapped = UserContactMapping(
                user=user,
                contact=contact
            ).save()

            response = {
                'msg': 'Contact saved successfully',
                'data': request.data
            }
            return Response(
                response,
                status=200,
                content_type="application/json"
            )


class SignupList(APIView):

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)

        user = User(
            username=username,
            password=password,
            email=email
        )

        user.set_password(password)
        user.save()

        user_profile = UserProfile(
            user=user,
            phone=phone
        ).save()

        if user:
            payload = {
                'id': user.id,
                'username': user.username,
            }

            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

            return Response(
                jwt_token,
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                json.dumps({'Error': "Error in signup"}),
                status=400,
                content_type="application/json"
            )


class LoginList(APIView):

    def post(self, request):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status=400)

        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (authenticate(username=username, password=password)):
            user = User.objects.get(username=username)
        else:
            return Response({'Error': "Invalid username/password"}, status=400)
        if user:
            payload = {
                'id': user.id,
                'username': user.username,
            }

            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

            return Response(
                jwt_token,
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                json.dumps({'Error': "Invalid credentials"}),
                status=400,
                content_type="application/json"
            )


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return ('', {'Error': "Token is invalid"})

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, "SECRET_KEY")
            username = payload['username']
            userid = payload['id']
            user = User.objects.get(
                username=username,
                id=userid,
                is_active=True
            )
        except:
            return ('', {'Error': "Token is invalid"})

        return (user, '')


class SpamList(APIView):
    def post(self, request):
        try:
            auth = TokenAuthentication()
            user, error = auth.authenticate(request)
            if (error):
                return Response(
                    error,
                    status=400,
                    content_type="application/json"
                )
            else:
                phone = request.data.get('phone', None)
                a = Contact.objects.filter(phone=phone).update(spam=True)
                b = UserProfile.objects.filter(phone=phone).update(spam=True)

                if (a + b):
                    return HttpResponse(
                        json.dumps({'message': "Contact marked as spam"}),
                        status=200,
                        content_type="application/json"
                    )
                else:
                    return HttpResponse(
                        json.dumps({'message': "Contact does not exist"}),
                        status=400,
                        content_type="application/json"
                    )

        except:
            return HttpResponse(
                json.dumps({'Error': "Internal server error"}),
                status=500,
                content_type="application/json"
            )


class SearchNameList(APIView):
    def get(self, request):
        try:
            auth = TokenAuthentication()
            user, error = auth.authenticate(request)
            if (error):
                return Response(
                    error,
                    status=400,
                    content_type="application/json"
                )
            else:
                name = request.GET.get('name', None)

                a = Contact.objects.all().filter(name=name)
                b = Contact.objects.all().filter(name__contains=name).exclude(name=name)

                response = []
                for contact in a:
                    response.append({
                        'name': contact.name,
                        'phone': contact.phone,
                        'spam': contact.spam
                    })
                for contact in b:
                    response.append({
                        'name': contact.name,
                        'phone': contact.phone,
                        'spam': contact.spam
                    })

                return Response(
                    response,
                    status=200,
                    content_type="application/json"
                )
        except:
            return HttpResponse(
                json.dumps({'Error': "Internal server error"}),
                status=500,
                content_type="application/json"
            )


class SearchPhoneList(APIView):
    def get(self, request):
        phone = request.GET.get('phone', None)

        try:
            auth = TokenAuthentication()
            user, error = auth.authenticate(request)
            if (error):
                return Response(
                    error,
                    status=400,
                    content_type="application/json"
                )
            else:
                profile = UserProfile.objects.get(phone=phone)

                if (profile):
                    user = User.objects.get(
                        id=profile.id,
                        is_active=True
                    )
                response = {
                    'name': user.username,
                    'phone': profile.phone,
                    'spam': profile.spam,
                    'email': user.email
                }

                return Response(
                    response,
                    status=200,
                    content_type="application/json"
                )

        except UserProfile.DoesNotExist:
            contacts = Contact.objects.all().filter(phone=phone)
            response = []
            for contact in contacts:
                response.append({
                    'name': contact.name,
                    'phone': contact.phone,
                    'spam': contact.spam,
                    'email': contact.email
                })

            return Response(
                response,
                status=200,
                content_type="application/json"
            )

        except:
            return HttpResponse(
                json.dumps({'Error': "Internal server error"}),
                status=500,
                content_type="application/json"
            )
