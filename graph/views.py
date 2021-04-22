from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from graph.serializer import ConnectNodeSerializer


class ConnectNode(GenericAPIView):
    serializer_class = ConnectNodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        graph = cache.get('graph', {})
        graph.update({data['start']: [data['end']]})
        cache.set("graph", graph)
        return Response("path set")


class Path(APIView):

    def get(self, request):
        start = request.query_params.get("start", None)
        end = request.query_params.get("end", None)
        graph = cache.get('graph', {})
        return Response(self.get_path(graph, start, end, path=[]) or 'no given path')

    @classmethod
    def get_path(cls, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        for node in graph[start]:
            if node not in path:
                new_path = cls.get_path(graph, node, end, path)
                if new_path: return new_path
        return None
