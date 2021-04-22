from django.urls import path

from graph.views import ConnectNode, Path

urlpatterns=[
    path('connect-node/',ConnectNode.as_view() ),
    path('path/',Path.as_view() ),

]