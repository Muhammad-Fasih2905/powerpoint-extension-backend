from rest_framework import serializers
from .models import *


# FlowchartSerializer
class FlowchartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ('id','title', 'data','description', 'image','type','diagram_type','user')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_url = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        # return f"{representation['id']}:{representation['title']}: {representation['data']}\nImage URL: {image_url}"
        return f"'id':{representation['id']}:\n'title':{representation['title']}:\n {representation['data']}\n'description':{representation['description']}\nImage URL: {image_url}"

class FlowchartSerializercopy(serializers.ModelSerializer):
    class Meta:
        model = Flowchart
        fields = ['data']
        

# GraphSerializer

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = ['id','title', 'data','description', 'image','type','diagram_type','user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_url = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        return f"'id':{representation['id']}:\n'title':{representation['title']}:\n {representation['data']}:\n'description':{representation['description']}\nImage URL: {image_url}"

#graph serilaizer copy
class GraphSerializerCopy(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = ['data']
        
        
# favorite digrams  

class FavoriteDiagramsSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField('get_pic')
    
    
    def get_pic(self, obj):
        graph = obj.graph
        flowchart = obj.flowchart

        if graph and hasattr(graph, 'image') and graph.image:
            return self.context['request'].build_absolute_uri(graph.image.url)
        elif flowchart and hasattr(flowchart, 'image') and flowchart.image:
            return self.context['request'].build_absolute_uri(flowchart.image.url)

        return None
    
    
    class Meta:
        model = SaveFavorite
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        graph = instance.graph
        flowchart = instance.flowchart
        if graph:
            graph_data = {
            'id':graph.id,
            'title':graph.title,
            'description':graph.description,
            'status':graph.status,
            'image': self.get_pic(instance),
            'type': graph.type,
            'diagram_type': graph.diagram_type,
            }
            response['graph'] = graph_data
        
        if flowchart:
            flowchart_data = {
            'id':flowchart.id,
            'title':flowchart.title,
            'description':flowchart.description,
            'status':flowchart.status,
            'image': self.get_pic(instance),
            'type': flowchart.type,
            'diagram_type': flowchart.diagram_type,
            
            
            }
            response['flowchart'] = flowchart_data
        return response
    

# copy
class SearchFavoriteDiagramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveFavorite
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        graph = instance.graph
        flowchart = instance.flowchart

        if graph:
            graph_data = {
            'id':graph.id,
            'title':graph.title,
            'description':graph.description,
            'status':graph.status,
            
            # 'image': graph.context['request'].build_absolute_uri(instance.image.url) if instance.image else None,
            'type': graph.type,
            }
            response['graph'] = graph_data
        
        if flowchart:
            flowchart_data = {
            'id':flowchart.id,
            'title':flowchart.title,
            'description':flowchart.description,
            'status':flowchart.status,
            # 'image': self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None,
            'type': flowchart.type,
            }
            response['graph'] = flowchart_data
        return response

    
            
            
            
class GraphsDiagramsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_pic')
    class Meta:
        model = Graph
        exclude = ['data']
        
    def get_pic(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    

        
class MermaidDiagramsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_pic')
    class Meta:
        model = Flowchart
        # fields = '__all__'
        exclude = ['data']
    
    def get_pic(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None