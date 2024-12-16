from django.contrib import admin

from api.Model import VennDiagram, ProblemStatement
from api.Model.ChannelMember import ChannelMember
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser
from api.Model.ProblemStatement import TwoVennProblemStatementModel, ThreeVennProblemStatementModel
from api.Model.Room import Room
from api.Model.RoomChannel import RoomChannel
from api.Model.RoomMember import RoomMember
from api.Model.Comment import Comment
from api.Model.RoomRequestJoin import RoomRequestJoin
from api.Model.SubmissionVoting import SubmissionVotingMark
from api.Model.VennDiagram import TwoVennDiagramModel, ThreeVennDiagramModel

admin.site.register(ChannelMember)
admin.site.register(ChannelSubmission)
admin.site.register(CustomUser)
admin.site.register(TwoVennProblemStatementModel)
admin.site.register(ThreeVennProblemStatementModel)
admin.site.register(Room)
admin.site.register(RoomChannel)
admin.site.register(RoomMember)
admin.site.register(Comment)
admin.site.register(TwoVennDiagramModel)
admin.site.register(ThreeVennDiagramModel)
admin.site.register(SubmissionVotingMark)
admin.site.register(RoomRequestJoin)