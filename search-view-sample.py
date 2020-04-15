from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Q

from post.serializers import PostListSerializer
from post.models import Post

from service.models import Service


def search_from_services_post(searching=None):
    results = {}
    if searching is None:
        results = {
            'results': None
        }

    searching_list = searching.split(' ')
    # just splitting the sentence into words

    # now posts time
    queries = [Q(title__icontains=search)
               for search in searching_list]
    query = queries.pop()
    for item in queries:
        query |= item

    posts = Post.objects.filter(query)
    post_serializer = PostListSerializer(posts, many=True)

    results['posts'] = post_serializer.data

    return results


class SearchApiView(APIView):
    def get(self, request, *args, **kwargs):
        searching = request.query_params.get('search', None)
        if searching:
            res = search_from_services_post(searching)
            return Response(res, status=status.HTTP_200_OK)
        return Response({'result': None}, status=status.HTTP_200_OK)
