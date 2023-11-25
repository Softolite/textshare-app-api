"""
Views for the content APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedOrReadOnly

from core.models import Content
from content import serializers


class ContentViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.ContentDetailSerializer
    queryset = Content.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pin'

    def get_queryset(self):
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # Return filtered queryset for authenticated users
            return self.queryset.filter(user=self.request.user).order_by('-id')
        else:
            # For unauthenticated, retrieve by a specific field ('pin')
            pin_param = self.kwargs.get('pin')  # Get 'pin' from URL path
            if pin_param is not None:
                # Return queryset filtered by the 'pin' field
                return self.queryset.filter(pin=pin_param)
            else:
                # Return an empty queryset by default for unauthenticated users
                return self.queryset.none()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContentSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new content."""
        serializer.save(user=self.request.user)
