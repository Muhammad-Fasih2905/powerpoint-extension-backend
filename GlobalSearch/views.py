from django.shortcuts import render
from visual.models import *
# from visual.serializers import *
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from visual.serializers import *
# Create your views here.




class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)

        if title is None:
            return Response({'error': 'Title cannot be None'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite_diagrams =  SaveFavorite.objects.filter(
            Q(graph__title__icontains=title) | Q(flowchart__title__icontains=title)
        )
        favorite_serializer = SearchFavoriteDiagramsSerializer(favorite_diagrams, many=True, context={'request': request})

        graphs_diagrams = Graph.objects.filter(title__icontains=title)
        graphs_serializer = GraphsDiagramsSerializer(graphs_diagrams, many=True ,context={'request': request})

        mermaid_diagrams = Flowchart.objects.filter(title__icontains=title)
        mermaid_serializer = MermaidDiagramsSerializer(mermaid_diagrams, many=True,context={'request': request})

        response_data = {
            'favorite_diagrams': favorite_serializer.data,
            'graphs_diagrams': graphs_serializer.data,
            'mermaid_diagrams': mermaid_serializer.data
        }

        return Response(response_data)

