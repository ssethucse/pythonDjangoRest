from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drinks.models import Drink
from drinks.serializers import DrinkSerializer


@api_view(['GET','POST'])
def drink_list(request, format=None):
    if request.method == 'GET':
        drink = Drink.objects.all()
        serializer = DrinkSerializer(drink,many=True)
        return Response(serializer.data)
        #return JsonResponse({'drinks':serializer.data},safe=False)
    if request.method == 'POST':
        serializer = DrinkSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def drink_details(request, id, format=None):
    try:
        drinks = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drinks)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drinks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        drinks.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
