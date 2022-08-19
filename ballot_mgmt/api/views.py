from rest_framework import viewsets, permissions, authentication, mixins, response
from django import http
from .models import BallotBox, Candidate
from .serializers import BallotBoxSerializer, CandidateSerializer

# Create your views here.
class BallotBoxView(viewsets.ModelViewSet):
    queryset = BallotBox.objects.all()
    serializer_class = BallotBoxSerializer
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
# Instead of inherit from ModelViewSet, we inherit from only necesary mixins
class CandidateView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    def get_queryset(self):
        # If ballot does not exist, raise 404
        try:
            BallotBox.objects.get(id=self.kwargs['bk'])
        except:
            raise http.Http404
        
        return Candidate.objects.filter(ballot_parent_id=self.kwargs['bk'])
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        if(self.request.method == 'POST'):
            context.update({"ballot_parent_id": self.kwargs['bk']})
            
        return context
    
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
