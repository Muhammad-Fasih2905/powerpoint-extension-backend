from django.urls import path, include
from .views import *
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'mermaid', FlowchartViewSet)
router.register(r'graphviz', GraphViewSet)
router.register(r'graph-diagrams',GraphsDiagramsViewSet,basename="graph-digrams")
router.register(r'mermaid-diagrams',MermaidDiagramsViewSet,basename="mermaid-digrams")
app_name = 'users'


urlpatterns = [
    path('', include(router.urls)),
    path('favorite_diagrams/',SaveFavoriteDiagramsAPIView.as_view(),),
    # path('test_favorite_diagrams/',TestSaveFavoriteDiagramsAPIView.as_view(),),
    path('get-mermaid-by-user/',GetMermaidDiagramsByUserId.as_view()),
    path('get-graph-by-user/',GetGraphDiagramsByUserId.as_view()),
]