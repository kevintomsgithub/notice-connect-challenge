from rest_framework import serializers
from .constants import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from .models import Notice, Record, Match
from .serializers import NoticeSerializer, RecordSerializer, MatchSerializer

# Create your views here.

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'list-all-notice': 'GET - /notices',
        'list-all-records': 'GET - /records',
        'list-all-matches': 'GET - /matches',
        'create-notice': 'POST - /notices',
        'create-record': 'POST - /records',
        'notice-details': 'GET - /notices/id',
        'record-details': 'GET - /notices/id',
        'delete-notice': 'DELETE - /notices/id',
        'delete-record': 'DELETE - /records/id',
    }
    return Response(api_urls)


class NoticeAPIViews(APIView):
    """
    API view for creating and listing notices
    """

    def get(self, request):
        # gets all notice from database
        notices = Notice.objects.all()
        # serialize all data
        serializer = NoticeSerializer(notices, many=True)
        # return serialized data
        return Response(serializer.data)

    def post(self, request):
        # serialize new notice data
        serializer = NoticeSerializer(data=request.data)
        # check if serialized data is valid
        if serializer.is_valid():
            # save data to database
            serializer.save()
            # return serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serialized data not valid
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class NoticeDetailsViews(APIView):
    """
    API view for getting details and deleting notice
    """

    def get_object(self, id):
        try:
            # return if notice found
            return Notice.objects.get(notice_id=id)
        except Notice.DoesNotExist:
            # return False if notice not found
            return False

    def delete_matches(self, notice_id):
        # find all matches
        matches = Match.objects.filter(notice_id=notice_id)
        # delete all matches found
        for match in matches:
            match.delete()

    def get(self, request, id):
        # get notice object
        notice = self.get_object(id)
        # if not notice object found
        if notice == False:
            # return no content status
            return Response(status=status.HTTP_204_NO_CONTENT)
        # serialize data
        serializer = NoticeSerializer(notice)
        # return data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        # get notice object
        notice = self.get_object(id)
        # if not notice object found
        if notice == False:
            # return no content status
            return Response(status=status.HTTP_204_NO_CONTENT)
        # delete all related matches
        self.delete_matches(notice_id=notice.notice_id)
        # delete notice
        notice.delete()
        # return no content status
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecordAPIViews(APIView):
    """
    API view for creating and listing notices
    """

    def get(self, request):
        # gets all records from database
        records = Record.objects.all()
        # serialize all data
        serializer = RecordSerializer(records, many=True)
        # return serialized data
        return Response(serializer.data)

    def post(self, request):
        # serialize new record data
        self.serializer = RecordSerializer(data=request.data)
        # check if serialized data is valid
        if self.serializer.is_valid():
            # perform match algorithm
            self._match_algorithm()
            # return serialized data
            return Response(self.serializer.data, status=status.HTTP_201_CREATED)
        # if serialized data not valid
        return Response(self.serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def _save_match(self, notice_obj, match_type):
        # save data to database
        self.serializer.save()
        # get record_id
        record_id = self.serializer.data['record_id']
        # iterate through all notice objects
        for notice in notice_obj:
            # save match object
            Match.objects.create(
                record_id=record_id,
                notice_id=notice.notice_id,
                match_type=match_type
            )

    def _match_algorithm(self):
        # get details from serializerd data
        first_name = self.serializer.validated_data['first_name']
        last_name = self.serializer.validated_data['last_name']
        province = self.serializer.validated_data['province']
        date_of_birth = self.serializer.validated_data['date_of_birth']
        # check for strong matches
        strong_match = Notice.objects.raw(
            "SELECT notice_id from api_notice \
             WHERE date_of_birth=%s AND \
                  (first_name=%s OR alt_first_name=%s) AND \
                  (last_name=%s OR alt_last_name=%s)", 
            [
                date_of_birth, first_name, first_name,
                last_name, last_name
            ]
        )
        # check for possible matches
        possible_match = Notice.objects.raw(
            "SELECT notice_id from api_notice \
             WHERE province=%s AND first_name=%s AND last_name=%s", 
            [
                province, first_name, last_name
            ]
        )
        # check for weak matches
        weak_match = Notice.objects.raw(
            "SELECT notice_id from api_notice \
             WHERE first_name=%s AND last_name=%s", 
            [
                first_name, last_name
            ]
        )
        # check for current match status
        if len(strong_match) > 0:
            # if strong match
            self._save_match(notice_obj=strong_match, match_type=STRONG_MATCH)
        elif len(possible_match) > 0:
            # if possible match
            self._save_match(notice_obj=possible_match, match_type=POSSIBLE_MATCH)
        elif len(weak_match) > 0:
            # if weak match
            self._save_match(notice_obj=weak_match, match_type=WEAK_MATCH)
        else:
            # if no match found
            self.serializer.save()


class RecordDetailsViews(APIView):
    """
    API view for getting details and deleting records
    """

    def get_object(self, id):
        try:
            # return if notice found
            return Record.objects.get(record_id=id)
        except Record.DoesNotExist:
            # return False if notice not found
            return False

    def delete_matches(self, record_id):
        # find all matches
        matches = Match.objects.filter(record_id=record_id)
        # delete all matches found
        for match in matches:
            match.delete()

    def get(self, request, id):
        # get record object
        record = self.get_object(id)
        # if not notice object found
        if record == False:
            # return no content status
            return Response(status=status.HTTP_204_NO_CONTENT)
        # serialize data
        serializer = RecordSerializer(record)
        # return data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        # get record object
        record = self.get_object(id)
        # if not record object found
        if record == False:
            # return no content status
            return Response(status=status.HTTP_204_NO_CONTENT)
        # delete all related matches
        self.delete_matches(record_id=record.record_id)
        # delete record
        record.delete()
        # return no content status
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatchAPIViews(APIView):
    """
    API view for listing all notices
    """

    def get(self, request):
        # gets all matches from database
        matches = Match.objects.all()
        # serialize all data
        serializer = MatchSerializer(matches, many=True)
        # return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)