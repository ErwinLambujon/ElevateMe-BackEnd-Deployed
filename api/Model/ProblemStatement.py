from django.db import models
from django.contrib.auth.models import User

from .CustomUser import CustomUser
from .VennDiagram import TwoVennDiagramModel, ThreeVennDiagramModel
class ProblemStatementModel(models.Model):
    statement = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TwoVennProblemStatementModel(ProblemStatementModel):
    venn = models.ForeignKey(TwoVennDiagramModel, on_delete=models.CASCADE)


class ThreeVennProblemStatementModel(ProblemStatementModel):
    venn = models.ForeignKey(ThreeVennDiagramModel, on_delete=models.CASCADE)
