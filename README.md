# BASE PATH: localhost:8000/api/

### Endpoints for User.
- GET `/user/` - This endpoint allows creating and querying a user.
- POST `/user/login/` - Login user which returns a token authentication.
- POST `/user/logout/` - Logout user and delete the token associated with the user.
- POST `/user/get_currently_login/` - Get user instance of currently login user.
  
### Endpoints for AI model.
- POST `/ai/two_venn/` - Prompt problem statement given two scopes.
- POST `/ai/three_venn/` - Prompt problem statement given three scopes.
- POST `/ai/potential_root/` - Prompt potential root given list of whys.
- POST `/ai/five_whys/` - Prompt five whys given ranked problem statement.
- POST `/ai/five_hmws/` - Prompt five whys given potential root problem.
- POST `/ai/elevator_pitch/` - Prompt elevator pitch given five How Might We's

### Endpoints for Problem Statements
- PUT `/two_venn_ps/` - Saves Problem statement fron the Two Venn Diagram setting.
- PUT `/three_venn_ps/` - Saves Problem statement fron the Three Venn Diagram setting.

### Endpoints for Room
- GET `/rooms/` -  Get all the rooms.
- GET `/rooms/:id/` - Get room by ID.
- GET `/rooms/:id/members/` - Get all members of a certain room.
- GET `/rooms/:id/channels/` - Get all the room's channels.
- GET `/rooms/auth_room/` - Get currently login user's joined room
- GET `/rooms/:id/applicants/` - Get all rooms applicants.
- POST `/rooms/` - Creates a room.
- PATCH - `/room/:id/` - Updates a room.
- POST `/rooms/:id/join/` - Request to join a room.
- POST `/rooms/:id/manage_request/` - Manage request application of a room.
- DELETE - `/room/:id/members/:member_id/` - Removes a room member

### Endpoints for Channel
- GET `/channels/` -  Get all the channel.
- GET `/channels/:id/` - Get channel by ID.
- GET `/channels/:id/members/` - Get all members of a certain channel.
- POST `/channels/` - Creates a channel.
- PATCH - `/channels/:id/` - Updates a channel.
- DELETE - `/channels/:id/members/:member_id/` - Removes a channel member

### Endpoints for Channel Submission
- GET `/channels/:id/submissions/` -  Get all the channels' submission.
- GET `/channels/:id/submissions/:channel_pk/` -  Get submission from a specific channel. 
- POST `/channels/:id/submissions/submit/` - Creates a submission

### Endpoints for Comments
- GET `/channels/:id/submissions/:id/comments/` - Get submission comments
- GET `/channels/:id/submissions/:id/comments/:id/` - Get specific submission comments
- POST `/channels/:id/submissions/:id/comments` - Creates a submission comment

### Endpoints for Submission Voting Marks
- GET `/channels/:id/submissions/:id/voting_marks/` - Get submission voting marks.
- GET `/channels/:id/submissions/:id/voting_marks/:id/` - Get specific submission voting marks.
- POST `/channels/:id/submissions/:id/voting_marks/` - Creates a submission voting marks.