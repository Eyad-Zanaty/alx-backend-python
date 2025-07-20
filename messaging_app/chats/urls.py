# chat/urls.py
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Main router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router for messages under a specific conversation
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
