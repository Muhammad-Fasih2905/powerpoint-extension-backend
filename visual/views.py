from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404

# Create your views here.


class FlowchartViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Flowchart.objects.all()
    serializer_class = FlowchartSerializer
    content_type = 'text/plain'

    
    def create(self, request, *args, **kwargs):
        user = request.user

        # Create a mutable copy of the QueryDict
        mutable_data = request.data.copy()

        # Add the user to the mutable data
        mutable_data['user'] = user.id
        serializer = FlowchartSerializer(data=mutable_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.validated_data)
        return HttpResponse(instance.data, content_type=self.content_type, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FlowchartSerializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(serializer.data, content_type=self.content_type)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FlowchartSerializercopy(instance, context={'request': request})
        return HttpResponse(f"{serializer.data['data']}", content_type=self.content_type)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = FlowchartSerializer(queryset, many=True, context={'request': request})
        return HttpResponse("\n\n".join(serializer.data), content_type=self.content_type)    

# graph
class GraphViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer
    content_type = 'text/plain'

    
    def create(self, request, *args, **kwargs):
        user = request.user
        # Create a mutable copy of the QueryDict
        mutable_data = request.data.copy()

        # Add the user to the mutable data
        mutable_data['user'] = user.id
        serializer = GraphSerializer(data=mutable_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.validated_data)
        return HttpResponse(instance.data, content_type=self.content_type, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GraphSerializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(serializer.data, content_type=self.content_type)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GraphSerializerCopy(instance, context={'request': request})
        return HttpResponse(f" {serializer.data['data']}", content_type=self.content_type)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GraphSerializer(queryset, many=True, context={'request': request})
        return HttpResponse("\n\n".join(serializer.data), content_type=self.content_type)
     
class GraphsDiagramsViewSet(viewsets.ModelViewSet):
    serializer_class = GraphsDiagramsSerializer
    
    def get_queryset(self):
        queryset = Graph.objects.all()
        title_parms = self.request.query_params.get('title',None)
        if title_parms:
            queryset = queryset.filter(title = title_parms,)
        serializer = GraphsDiagramsSerializer(queryset, context={'request': self.request}, many=True)
        return queryset
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # grouped_data = self.group_by_type(queryset)
        serializer = GraphsDiagramsSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
    

    
    def group_by_type(self, queryset):
        grouped_data = {}
        for graph in queryset:
            type_key = graph.type
            if type_key not in grouped_data:
                grouped_data[type_key] = []
            grouped_data[type_key].append(
                GraphsDiagramsSerializer(graph, context={'request': self.request}).data
            )
        return grouped_data
    
class MermaidDiagramsViewSet(viewsets.ModelViewSet):
    serializer_class = MermaidDiagramsSerializer
    
    def get_queryset(self):
        queryset = Flowchart.objects.all()
        title_parms = self.request.query_params.get('title',None)
        if title_parms:
            queryset = queryset.filter(title = title_parms,)
        serializer = MermaidDiagramsSerializer(queryset, context={'request': self.request}, many=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # grouped_data = self.group_by_type(queryset)
        serializer = MermaidDiagramsSerializer(queryset, context={'request': request}, many=True)
        # return Response(grouped_data)
        return Response(serializer.data)

    
    def group_by_type(self, queryset):
        grouped_data = {}
        for graph in queryset:
            type_key = graph.type
            if type_key not in grouped_data:
                grouped_data[type_key] = []
            grouped_data[type_key].append(
                MermaidDiagramsSerializer(graph, context={'request': self.request}).data
            )
        return grouped_data
  


# digram get by user_id
class GetMermaidDiagramsByUserId(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = user_id = request.user.id
        flowchart_data = Flowchart.objects.filter(user=user_id)

         # Serialize the data
        flowchart_serializer = MermaidDiagramsSerializer(flowchart_data,context={'request': self.request}, many=True)


        # Return the serialized data as a response
        response_data = {
            'flowchart': flowchart_serializer.data,
        }

        return Response(flowchart_serializer.data, status=status.HTTP_200_OK)

class GetGraphDiagramsByUserId(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
 
        graph_data = Graph.objects.filter(user=user_id)
         # Serialize the data
        graph_serializer = GraphsDiagramsSerializer(graph_data,context={'request': self.request}, many=True)
        # Return the serialized data as a response
        response_data = {

            'graph': graph_serializer.data,
        }

        return Response(graph_serializer.data, status=status.HTTP_200_OK)

# test_onnedrive
class SaveFavoriteDiagramsAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        github_token = request.data.get("github_token")
        onedrive_token = request.data.get("onedrive_token")
        
        
        if (github_token is None and onedrive_token is None) or (github_token is not None and onedrive_token is not None):
            return Response({"error": "Either GitHub token or OneDrive token (but not both) is required in the request body"}, status=400)
        
            # Make a request to the GitHub API
        github_api_url = "https://api.github.com/user"
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get(github_api_url, headers=headers)

        # Check if the request was successful
        if github_token:
            
            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")
                flowchart = request.data.get("flowchart")
                graph = request.data.get("graph")
                
                if flowchart:
                    if SaveFavorite.objects.filter(flowchart=flowchart,github_user_id=user_id).exists():
                        return Response({"detail": "You have already saved this flowchart."}, status=status.HTTP_400_BAD_REQUEST)
                if graph:
                    if SaveFavorite.objects.filter(graph=graph,github_user_id=user_id).exists():
                        return Response({"detail": "You have already saved this graph."}, status=status.HTTP_400_BAD_REQUEST)
                
                save_favorite_data = {
                    "github_user_id": user_id,
                    "graph": graph,
                    "flowchart": flowchart,
                    "status": True, 
                }
                serializer = FavoriteDiagramsSerializer(data=save_favorite_data, context={'request': self.request})
                

                if serializer.is_valid():
                    # serializer.save()
                    favorite_diagram = serializer.save()
                    if graph:
                        graph_instance = favorite_diagram.graph 
                        graph_instance.status = True
                        graph_instance.save()
                        
                        # Save the graph data to GitHub Gists
                        gist_api_url = "https://api.github.com/gists"           
                        gist_data = {
                            "description": "Graph saved by your application",
                            "public": False,
                            "files": {
                                f" {graph_instance.title}": {
                                    "content": f"{graph_instance.data}"
                                }
                                    }
                            }
                            
                        gist_response = requests.post(gist_api_url, headers=headers, json=gist_data)
                        # ONE DRIVE
                        onedrive_filename = f"{graph_instance.title}.txt"
                        onedrive_url = f'https://graph.microsoft.com/v1.0/me/drive/root:/{onedrive_filename}:/content'
                        onedrive_headers = {'Authorization': f'Bearer {onedrive_token}', 'Content-Type': 'text/plain'}

                        onedrive_response = requests.put(onedrive_url, headers=onedrive_headers, data=graph_instance.data)
                        print('onedrive_response',onedrive_response)

                        if gist_response.status_code == 201:
                            gist_id = gist_response.json()['id']
                            favorite_diagram.gist_id = gist_id
                            favorite_diagram.save()
                            serialized_data = FavoriteDiagramsSerializer(favorite_diagram, context={'request': self.request}).data
                            serialized_data["gist_url"] = gist_api_url
                            return Response({"detail": "Graph and Gist saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
                          
                        else:
                            error_message = gist_response.json().get("message", "Unknown error")
                            return Response({"error": f"Error Graph Post Gist: {error_message}","data": serializer.data}, status=gist_response.status_code)
                        
                        
                    if flowchart:
                        flowchart_instance = favorite_diagram.flowchart  
                        flowchart_instance.status = True
                        flowchart_instance.save()
                        gist_api_url = "https://api.github.com/gists"
                        
                        gist_data = {
                            "description": "Flowchart saved by your application",
                            "public": False,
                            "files": {
                                f" {flowchart_instance.title}": {
                                    "content": f"{flowchart_instance.data}"
                                }
                                    }
                        }
                        gist_response = requests.post(gist_api_url, headers=headers, json=gist_data)
                        
                        
                        onedrive_filename = f"{flowchart_instance.title}.txt"
                        onedrive_url = f'https://graph.microsoft.com/v1.0/me/drive/root:/{onedrive_filename}:/content'
                        onedrive_headers = {'Authorization': f'Bearer {onedrive_token}', 'Content-Type': 'text/plain'}
                        onedrive_response = requests.put(onedrive_url, headers=onedrive_headers, data=flowchart_instance.data)
                        print('onedrive_response',onedrive_response)
                        
                        if gist_response.status_code == 201:
                            gist_id = gist_response.json()['id']
                            favorite_diagram.gist_id = gist_id
                            favorite_diagram.save()
                            # Gist created successfully, you can retrieve the gist URL from gist_response.json()["html_url"]
                            serialized_data = FavoriteDiagramsSerializer(favorite_diagram, context={'request': self.request}).data
                            serialized_data["gist_url"] = gist_api_url
                        
                            return Response({"detail": "Flowchart and Gist saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
                        elif onedrive_response.status_code == 201:
                            # oneDriveId = onedrive_response.json().get("id")
                            # favorite_diagram.oneDriveId = oneDriveId
                            # favorite_diagram.save()
                            # serialized_data["OneDriveUrl"] = onedrive_api_url + "/" + oneDriveId
                            return Response({"detail": "Flowchart and OneDrive saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
                        else:
                            # Handle error when creating the gist
                            error_message = gist_response.json().get("message", "Unknown error")
                            return Response({"error": f"Error Flowchart Post Gist: {error_message}","data": serializer.data}, status=gist_response.status_code)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"error": "Failed to retrieve user data from GitHub"}, status=response.status_code)
        
        if onedrive_token:
            graph_url = 'https://graph.microsoft.com/v1.0/me'
            headers = {'Authorization': f'Bearer {onedrive_token}'}
            graph_response = requests.get(graph_url, headers=headers)
            if graph_response.status_code == 200:
                user_data = graph_response.json()
                onedrive_file_location = graph_response.json().get('parentReference', {}).get('path', '')
                onedrive_file_id = graph_response.json().get('id', '')
                print("user-data",user_data)
                user_id = user_data.get("id")
                
                flowchart = request.data.get("flowchart")
                graph = request.data.get("graph")
                
                if flowchart:
                    if SaveFavorite.objects.filter(flowchart=flowchart,onedrive_user_id=user_id).exists():
                        return Response({"detail": "You have already saved this flowchart."}, status=status.HTTP_400_BAD_REQUEST)
                if graph:
                    if SaveFavorite.objects.filter(graph=graph,onedrive_user_id=user_id).exists():
                        return Response({"detail": "You have already saved this graph."}, status=status.HTTP_400_BAD_REQUEST)
                
                save_favorite_data = {
                    "onedrive_user_id": user_id,
                    "graph": graph,
                    "flowchart": flowchart,
                    "status": True, 
                }
                serializer = FavoriteDiagramsSerializer(data=save_favorite_data, context={'request': self.request})
                
                if serializer.is_valid():
                    # serializer.save()
                    favorite_diagram = serializer.save()
                    if graph:
                        graph_instance = favorite_diagram.graph 
                        graph_instance.status = True
                        graph_instance.save()
                        
                        # ONE DRIVE
                        onedrive_filename = f"{graph_instance.title}.txt"
                        onedrive_url = f'https://graph.microsoft.com/v1.0/me/drive/root:/{onedrive_filename}:/content'
                        onedrive_headers = {'Authorization': f'Bearer {onedrive_token}', 'Content-Type': 'text/plain'}

                        onedrive_response = requests.put(onedrive_url, headers=onedrive_headers, data=graph_instance.data)

                        if onedrive_response.status_code == 201:
                            onedrive_user_id = graph_response.json()['id']
                            onedrive_file_location = onedrive_response.json()['id']
                            favorite_diagram.onedrive_user_id = onedrive_user_id
                            favorite_diagram.onedrive_url=onedrive_file_location
                            favorite_diagram.save()
                            serialized_data = FavoriteDiagramsSerializer(favorite_diagram, context={'request': self.request}).data
                            return Response({"detail": "Graph and OneDrive Data saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
                          
                        else:
                            error_message = onedrive_response.json().get("message", "Unknown error")
                            return Response({"error": f"Error Graph Post OneDrive: {error_message}","data": serializer.data}, status=onedrive_response.status_code)
                        
                        
                    if flowchart:
                        flowchart_instance = favorite_diagram.flowchart  
                        flowchart_instance.status = True
                        flowchart_instance.save()
                        
                        
                        onedrive_filename = f"{flowchart_instance.title}.txt"
                        onedrive_url = f'https://graph.microsoft.com/v1.0/me/drive/root:/{onedrive_filename}:/content'
                        onedrive_headers = {'Authorization': f'Bearer {onedrive_token}', 'Content-Type': 'text/plain'}
                        onedrive_response = requests.put(onedrive_url, headers=onedrive_headers, data=flowchart_instance.data)
                        
                        if onedrive_response.status_code == 201:
                            onedrive_user_id = graph_response.json()['id']
                            onedrive_file_location = onedrive_response.json()['id']
                            favorite_diagram.onedrive_user_id = onedrive_user_id
                            favorite_diagram.onedrive_url=onedrive_file_location
                            favorite_diagram.save()
                            # Gist created successfully, you can retrieve the gist URL from gist_response.json()["html_url"]
                            serialized_data = FavoriteDiagramsSerializer(favorite_diagram, context={'request': self.request}).data
                            # serialized_data["gist_url"] = gist_api_url
                        
                            return Response({"detail": "Flowchart and OneDrive saved successfully", "data": serialized_data}, status=status.HTTP_201_CREATED)
                        else:
                            # Handle error when creating the gist
                            error_message = onedrive_response.json().get("message", "Unknown error")
                            return Response({"error": f"Error Flowchart Post OneDrive: {error_message}","data": serializer.data}, status=onedrive_response.status_code)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"Error":'Failed to retrieve user data from OneDrive'})
        
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            
    
    def get(self, request, *args, **kwargs):
        github_token = request.query_params.get("github_token")
        onedrive_token = request.query_params.get("onedrive_token")

        if (github_token is None and onedrive_token is None) or (github_token is not None and onedrive_token is not None):
            return Response({"error": "Either GitHub token or OneDrive token (but not both) is required in the request body"}, status=400)

        if github_token:
            github_api_url = "https://api.github.com/user"
            headers = {"Authorization": f"token {github_token}"}
            response = requests.get(github_api_url, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")
                user_answers = SaveFavorite.objects.filter(github_user_id=user_id, status=True)

                serializer = FavoriteDiagramsSerializer(user_answers, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to retrieve user data from GitHub"}, status=response.status_code)

        if onedrive_token:
            onedrive_url = 'https://graph.microsoft.com/v1.0/me'
            headers = {'Authorization': f'Bearer {onedrive_token}'}
            response = requests.get(onedrive_url, headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")
                user_answers = SaveFavorite.objects.filter(onedrive_user_id=user_id, status=True)

                serializer = FavoriteDiagramsSerializer(user_answers, many=True, context={'request': self.request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to retrieve user data from OneDrive"}, status=response.status_code)

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, *args, **kwargs):
        github_token = request.query_params.get("github_token")
        onedrive_token = request.query_params.get("onedrive_token")  #add new
        flowchart_id = request.query_params.get("flowchart")
        graph_id = request.query_params.get("graph")
        
        

        if (github_token is None and onedrive_token is None) or (github_token is not None and onedrive_token is not None):
            return Response({"error": "Either GitHub token or OneDrive token (but not both) is required in the request body"}, status=400)
        
        if github_token:
            # Make a request to the GitHub API
            github_api_url = "https://api.github.com/user"
            headers = {"Authorization": f"token {github_token}"}
            response = requests.get(github_api_url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")

                save_favorite_instance = None

                if flowchart_id:
                    print("flowchart",flowchart_id)
                    # Update the Flowchart instance status
                    flowchart_instance = Flowchart.objects.filter(id=flowchart_id).first()
                    if flowchart_instance:
                        flowchart_instance.status = False
                        flowchart_instance.save()

                        # Get the corresponding SaveFavorite instance
                        save_favorite_instance = SaveFavorite.objects.filter(flowchart=flowchart_instance, github_user_id=user_id).first()
                        print("in flowchart save",save_favorite_instance)

                elif graph_id:
                    # Update the Graph instance status
                    graph_instance = Graph.objects.filter(id=graph_id).first()
                    if graph_instance:
                        graph_instance.status = False
                        graph_instance.save()

                        # Get the corresponding SaveFavorite instance
                        save_favorite_instance = SaveFavorite.objects.filter(graph=graph_instance, github_user_id=user_id).first()

                if save_favorite_instance:
                    # Delete the corresponding Gist from GitHub
                    gist_id = save_favorite_instance.gist_id

                    if gist_id:
                        # Make a request to the GitHub Gists API to delete the Gist
                        gist_api_url = f"https://api.github.com/gists/{gist_id}"
                        delete_response = requests.delete(gist_api_url, headers=headers)

                        # Check if the Gist deletion was successful
                        if delete_response.status_code == 204:
                            # Delete the SaveFavorite instance
                            save_favorite_instance.delete()
                            return Response({"detail": "Gist and instance deleted successfully"}, status=status.HTTP_200_OK)
                            # return Response({"detail": "Gist and instance deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                            # return Response({"detail": "Gist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                        else:
                            return Response({"error": "Failed to delete Gist"}, status=delete_response.status_code)
                    else:
                        return Response({"error": "gist_id not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": "SaveFavorite instance not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Failed to fetch user data from GitHub"}, status=response.status_code)
            
        if onedrive_token:
            # Make a request to the OneDrive API
            graph_url = 'https://graph.microsoft.com/v1.0/me'
            headers = {'Authorization': f'Bearer {onedrive_token}'}
            # graph_response = requests.get(graph_url, headers=headers)
            response = requests.get(graph_url, headers=headers)


            # Check if the request was successful
            if response.status_code == 200:
                drive_data = response.json()
                drive_id = drive_data.get("id")

                save_favorite_instance = None

                if flowchart_id:
                    print("flowchart", flowchart_id)
                    # Update the Flowchart instance status
                    flowchart_instance = Flowchart.objects.filter(id=flowchart_id).first()
                    if flowchart_instance:
                        flowchart_instance.status = False
                        flowchart_instance.save()

                        # Get the corresponding SaveFavorite instance
                        save_favorite_instance = SaveFavorite.objects.filter(flowchart=flowchart_instance, onedrive_user_id=drive_id).first()
                        
                elif graph_id:
                    # Update the Graph instance status
                    graph_instance = Graph.objects.filter(id=graph_id).first()
                    if graph_instance:
                        graph_instance.status = False
                        graph_instance.save()

                        # Get the corresponding SaveFavorite instance
                        save_favorite_instance = SaveFavorite.objects.filter(graph=graph_instance, onedrive_user_id=drive_id).first()

                if save_favorite_instance:
                    # Delete the corresponding file/folder from OneDrive
                    file_id = save_favorite_instance.onedrive_url

                    if file_id:
                        # Make a request to the OneDrive API to delete the file/folder
                        onedrive_api_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
                        delete_response = requests.delete(onedrive_api_url, headers=headers)

                        # Check if the deletion was successful
                        if delete_response.status_code == 204:
                            # Delete the SaveFavorite instance
                            save_favorite_instance.delete()
                            return Response({"detail": "File/Folder and instance deleted successfully"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": "Failed to delete file/folder from OneDrive"}, status=delete_response.status_code)
                    else:
                        return Response({"error": "file_id not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": "SaveFavorite instance not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Failed to fetch user data from OneDrive"}, status=response.status_code)
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)






























