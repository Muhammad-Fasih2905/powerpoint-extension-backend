from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Flowchart)
class FlowchartAdmn(admin.ModelAdmin):
    list_display = ['id','title','image','description']
    
    


@admin.register(Graph)
class GraphAdmn(admin.ModelAdmin):
    list_display = ['id','title','image','description']
    
    
    

    
    
    
    
    
    
    
    
@admin.register(SaveFavorite)
class SaveFavoriteAdmn(admin.ModelAdmin):
    list_display = ['id','graph','flowchart','created','updated']