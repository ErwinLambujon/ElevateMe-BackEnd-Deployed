from aiohttp.web_routedef import static
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .View import *
from .View.ChannelSubmissionView import ChannelSubmissionView
from .View.ProblemStatementView import TwoVennProblemStatementView, ThreeVennProblemStatementView
from .View.RoomChannelView import RoomChannelView
from .View.RoomView import RoomView
from .View.SubmissionCommentView import SubmissionCommentView
from .View.SubmissionVotingView import SubmissionVotingMarkView

# Main Router
router = SimpleRouter()
router.register('user', UserView)
router.register('ai', GPTApiView, basename='ai')
router.register('two_venn_ps', TwoVennProblemStatementView)
router.register('three_venn_ps', ThreeVennProblemStatementView)
router.register('rooms', RoomView)
router.register('channels', RoomChannelView)

# First Nested Router: Submissions nested under Channels
submission_router = routers.NestedSimpleRouter(
    router,
    r'channels',
    lookup='channel'
)
submission_router.register(
    r'submissions',
    ChannelSubmissionView,
    basename='submissions'
)

# Second Nested Router: Comments nested under Submissions
comment_router = routers.NestedSimpleRouter(
    submission_router,
    r'submissions',
    lookup='submission'
)

comment_router.register(
    r'comments',
    SubmissionCommentView,
    basename='comment'
)

# Third Nested Router: Voting nested under Submissions
voting_router = routers.NestedSimpleRouter(
    submission_router,
    r'submissions',
    lookup='submission'
)
voting_router.register(
    r'voting_marks',
    SubmissionVotingMarkView,
    basename='voting_marks'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(submission_router.urls)),
    path('', include(comment_router.urls)),
    path('', include(voting_router.urls)),
]