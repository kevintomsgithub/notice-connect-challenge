from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'list-all-notice': 'GET - /notices',
        'list-all-records': 'GET - /records',
        'list-all-matches': 'GET - /matches',
        'create-notice': 'POST - /notices',
        'create-record': 'POST - /records',
        'notice-details': 'GET - /notice/id',
        'record-details': 'GET - /notice/id',
        'delete-notice': 'DELETE - /notice/id',
        'delete-record': 'DELETE - /record/id',
    }
    return Response(api_urls)