from datetime import datetime, timezone
from rest_framework import viewsets, permissions, authentication, mixins, response, status
from django import http, shortcuts
from .models import BallotBox, Candidate
from .serializers import BallotBoxCreateOrUpdateSerializer, BallotBoxListSerializer, BallotBoxRetrieveSerializer, CandidateCreateSerializer, CandidateListSerializer

# Create your views here.
class BallotBoxView(viewsets.ModelViewSet):
    queryset = BallotBox.objects.all()
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    def get_serializer_class(self):
        if(self.action == 'list'):
            return BallotBoxListSerializer
        if(self.action == 'retrieve'):
            return BallotBoxRetrieveSerializer
        if(self.action == 'create' or self.action == 'update' or self.action == 'partial_update'):
            return BallotBoxCreateOrUpdateSerializer
    
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
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    # As we don't want all candidates, instead of using queryset attribute, we have get filter the ones we want
    def get_queryset(self):
        try:
            return shortcuts.get_list_or_404(Candidate, ballot_parent_id=self.kwargs['bk'])
        except:
            try:
                shortcuts.get_object_or_404(BallotBox, id=self.kwargs['bk'])
                return []
            except:
                raise http.Http404
    
    def get_object(self):
        try:
            return shortcuts.get_object_or_404(Candidate, ballot_parent_id = self.kwargs['bk'], pk_inside_ballot = self.kwargs['pk'])
        except:
            raise http.Http404
    
    # As the ballot and the candidate number on ballot aren't provided by the user, we pass them to the serializer as context on POST calls
    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        if(self.request.method == 'POST'):
            context.update({"ballot_parent_id": self.kwargs['bk']})

            last_candidate_for_ballot = Candidate.objects.order_by('pk_inside_ballot').filter(ballot_parent_id=self.kwargs['bk']).last()
            
            if last_candidate_for_ballot is not None:
                context.update({"last_candidate_id": last_candidate_for_ballot.pk_inside_ballot})
            else:
                context.update({"last_candidate_id": 0})
            
        return context
    
    def get_serializer_class(self):
        if(self.action == 'list'):
            return CandidateListSerializer
        if(self.action == 'create'):
            return CandidateCreateSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
