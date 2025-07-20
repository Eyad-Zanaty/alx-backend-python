# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    CreateConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer,
)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateConversationSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save()
        # You can optionally add the request.user to the conversation:
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs['conversation_pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMessageSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_pk']
        serializer.save(
            sender=self.request.user,
            conversation=Conversation.objects.get(pk=conversation_id)
        )
