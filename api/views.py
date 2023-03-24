from django.shortcuts import render
from rest_framework import viewsets, status
from . models import Meal, Rating
from . serializer import MealSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'token': token.key,
        },
        status=status.HTTP_201_CREATED)
        
    def list(self, request, *args, **kwargs):
        response = {
            'message' : 'You cant created tating like thet'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            '''
            create or update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            # username = request.data['username']    becouse i used token
            # user = User.objects.get(username=username)
            
            try:
                # update
                rating = Rating.objects.get(user=user.id, meal=meal.id)
                rating.stars = stars
                rating.save()
                serializers = RatingSerializer(rating, many=False)
                json = {
                    'message' : 'Meal Rate Updated',
                    'result' : serializers.data
                }
                return Response(json , status=status.HTTP_200_OK)
                
            except:     
                # create
                rating = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializers = RatingSerializer(rating, many=False)
                json = {
                    'message' : 'Meal Rate Created',
                    'result' : serializers.data
                }
                return Response(json, status=status.HTTP_201_CREATED)
        else:
            json = {
                    'message' : 'Stars Not Provided',
                }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)
    
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer    
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def update(self, request, *args, **kwargs):
        response = {
            'message' : 'Invalid way to created or updated'
                
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message' : 'Invalid way to created or updated'
                
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)