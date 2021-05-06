from rest_framework.test import APITestCase
from django.shortcuts import reverse
from django.core.cache import cache


class TestGraph(APITestCase):


    def setUp(self) -> None:
        self.set_path_uri=reverse('connect_node')
        self.get_path_uri=reverse('path')

    def test_set_and_get_only_path(self):
        response=self.client.post(self.set_path_uri,data={"start":"A","end":"B"})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,"path set")
        response = self.client.get(f"{self.get_path_uri}?start=A&end=B")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ["A","B"])

    def test_set_and_get_shortest_path(self):
        response=self.client.post(self.set_path_uri,data={"start":"A","end":"B"})
        self.assertEqual(response.status_code,200)
        response = self.client.post(self.set_path_uri, data={"start": "A", "end": "C"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.set_path_uri, data={"start": "B", "end": "C"})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{self.get_path_uri}?start=A&end=C")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ["A","C"])
        self.assertEqual(cache.get('graph'),{"A":{"B","C"},"B":{"C"}})

    def test_set_path_wrong_input_key(self):
        response=self.client.post(self.set_path_uri,data={"wrong":"A","input":"B"})
        self.assertEqual(response.status_code,400)

    def test_get_path_not_exist(self):
        response = self.client.get(f"{self.get_path_uri}?start=A&end=B")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'no given path')

