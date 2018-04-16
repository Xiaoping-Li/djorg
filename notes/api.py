from rest_framework import serializers, viewsets
from .models import Note

# Serializers define the API representation
class NoteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Note
		fields = ('title', 'content')
	# create a node and return the node, overwrite the create method from serializer
	def create(self, validated_data):
		user = self._context['request'].user
		note = Note.objects.create(user=user, **validated_data)
		return note

# viewsets define the view behavior
class NoteViewSet(viewsets.ModelViewSet):
	serializer_class = NoteSerializer
	queryset = Note.objects.none()

	# overwrite the method get_query
	def get_queryset(self):
		user = self.request.user
		if user.is_anonymous:
			return Note.objects.none()
		else:
			return Note.objects.filter(user=user)
