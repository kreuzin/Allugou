from django.shortcuts import render, get_object_or_404
from AllugouApp.models import *
from AllugouApp.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response




@api_view()
def test(request):
    return Response({"message": "view is working"})

#tem esse jeito com api_view e tem um mais manero com classe eu acho dps vejo

@api_view(['GET', 'POST'])
def Enderecos_list(request): #get enderecos ou post -- senhor obvious

    if request.method == 'GET':
        enderecos = Endereco.objects.all() #acho q isso eh um queryset - v

        serializer = EnderecoSerializer(enderecos, many = True) #(enderecos, many=True) na documentacao se nao tive da erro de queryset

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = EnderecoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        #else
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



