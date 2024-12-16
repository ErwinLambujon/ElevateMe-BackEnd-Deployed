from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from abc import ABC, abstractmethod

from ..Serializer.ProblemStatementSerializer import TwoVennProblemStatementSerializer, \
    ThreeProblemStatementSerializer

from ..Model.ProblemStatement import TwoVennProblemStatementModel, ThreeVennProblemStatementModel


class AbstractVennProblemStatementView(ABC, mixins.ListModelMixin,
                                       mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @abstractmethod
    def get_queryset(self):
        pass

    @abstractmethod
    def get_serializer_class(self):
        pass

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Saved Problem Statement"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TwoVennProblemStatementView(AbstractVennProblemStatementView):
    queryset = TwoVennProblemStatementModel.objects.all()
    serializer_class = TwoVennProblemStatementSerializer

    def get_queryset(self):
        return TwoVennProblemStatementModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class

class ThreeVennProblemStatementView(AbstractVennProblemStatementView):
    queryset = ThreeVennProblemStatementModel.objects.all()
    serializer_class = ThreeProblemStatementSerializer

    def get_queryset(self):
        return ThreeVennProblemStatementModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class
