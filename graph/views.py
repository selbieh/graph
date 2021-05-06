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
        if graph.get(data['start'],None) == None:
            graph[data['start']] = set(data['end'])
        else:
            graph[data['start']].add(data['end'])
        cache.set("graph", graph)
        return Response("path set")


class Path(APIView):

    def get(self, request):
        start = request.query_params.get("start", None)
        end = request.query_params.get("end", None)
        graph = cache.get('graph', {})
        return Response(self.find_shortest_path(graph, start, end) or 'no given path')

    @staticmethod
    def find_shortest_path(graph, start, end):
        explored = []
        queue = [[start]]
        if start == end:
            return [start]
        while queue:
            path = queue.pop(0) #path == [start] ,a==[]
            node = path[-1]  #node = start
            if node not in explored:
                connected_nodes = graph.get(node,None)
                if connected_nodes:
                    for connected_node in connected_nodes:
                        new_path = list(path)
                        new_path.append(connected_node)
                        queue.append(new_path)
                        if connected_node == end:
                            return new_path
                    explored.append(node)
        return None