from django.db import models
from users.models import User
import os
# Create your models here.

def flowchart_image_path(instance, filename):
        return os.path.join('Flowchart_Pictures', 'Flowchart_Picture_%s' % instance.id, filename)

class Flowchart(models.Model):
        
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name="user_flowchart")
    title = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(('Flowchart Picture'), upload_to=flowchart_image_path, null=True, blank=True)
    data = models.TextField()
    description = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=200,null=True, blank=True)
    diagram_type = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Flowchart {self.pk}"


def graph_image_path(instance, filename):
        return os.path.join('Graph_Pictures', 'Graph_Picture_%s' % instance.id, filename)


class Graph(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name="user_graph")
    title = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(('Graph Picture'), upload_to=graph_image_path, null=True, blank=True)
    data = models.TextField()
    description = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=200,null=True, blank=True)
    github_username = models.CharField(max_length=255, null=True, blank=True)
    diagram_type = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    

    def __str__(self):
        return f"Graph {self.pk}"








class SaveFavorite(models.Model):
        github_user_id = models.IntegerField(null=True, blank=True)
        onedrive_user_id = models.CharField(max_length=300,null=True, blank=True)
        onedrive_url =models.TextField(blank=True,null=True)
        gist_id = models.CharField(max_length=200,blank=True,null=True)
        graph = models.ForeignKey(Graph,on_delete=models.CASCADE,null=True,
                                  blank=True,related_name="favorite_graph")
        flowchart = models.ForeignKey(Flowchart,on_delete=models.CASCADE,null=True,
                                      blank=True,related_name="favorite_graph")
        status = models.BooleanField(default=True)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)