from django.db import models

from django.contrib.auth.models import User

from api.Model.CustomUser import CustomUser


class VennDiagramModel(models.Model):
    field1 = models.TextField(null=False)
    field2 = models.TextField(null=False)
    filter = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class TwoVennDiagramModel(VennDiagramModel):
    def __str__(self):
        return f"{self.field1} | {self.field2}"

class ThreeVennDiagramModel(VennDiagramModel):
    field3 = models.TextField(null=False)
    def __str__(self):
        return f"{self.field1} | {self.field2} | {self.field3}"