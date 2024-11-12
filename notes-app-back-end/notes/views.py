from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.serializers import NoteSerializer
from .models import Note

class NoteList(APIView):
    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid(raise_exception=True):
            note = serializer.save()
            return Response({
                    "id": note.id
            }, status=201)

        return Response(serializer.errors, status=400)

    def get(self, request, format=None):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request': request})  # Pass request context
        return Response({
            "notes": serializer.data
        }, status=200)

class NoteDetail(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            note = serializer.save()
            return Response({"id": note.id}, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        return Response(status=204)
