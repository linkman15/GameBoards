# -*- coding: utf-8 -*-
# try something like
def index():
    users = db.auth_user
    
    def generate_view_button(row):
        # Views the group
        b = A('View', _class='btn', _href=URL('users', 'user', args=[row.username]))
        return b
    
    @auth.requires_login()
    def generate_friend_button(row):
        b = ''
        if auth.user.id != row.id:
            b = A('Add Friend', _class='btn', _href=URL('users', 'add_friend', args=[row.username]))
        return b
    
    @auth.requires_login()
    def generate_message_button(row):
        b = ''
        if auth.user.id != row.id:
            b = A('Send Message', _class='btn', _href=URL('users', 'send_message', args=[row.username]))
        return b
    
    links = [
        dict(header='', body = generate_view_button),
        dict(header='', body = generate_friend_button),
        dict(header='', body = generate_message_button),
    ]
    
    form = SQLFORM.grid(users, args=request.args[:0],
                        fields=[users.username],
        editable=False, deletable=False, details = False, 
        csv = False,
        create = False,
        links=links,
        paginate=50,
        )
    
    return dict(form=form)

def user():
    #user_id = db.auth_user.username == request.args(0) or redirect('users', 'index')
    user = db(db.auth_user.username == request.args(0)).select().first() or redirect('users', 'index')
    form = ''
    
    if request.args(0) == auth.user.username:
        redirect(URL('users', 'profile'))
        
    return dict(user=user, form=form)

def profile():
    user=auth.user
    user_form = db(db.auth_user.username == user.username).select().first()
    #form = SQLFORM(db.auth_user, fields = ['username', 'friends', 'games', 'groups', 'info'], readonly=True, record=auth.user)
    form = SQLFORM.factory(#Field('username', label='Username', default=user.username, writable=False),
                           #Field('friends', label='Friends', default=user.friends, writable=False),
                           #Field('games', label='Games', default=user.games, writable=False),
                           #Field('groups', label='Groups', default=user.groups, writable=False),
                           Field('info', 'text', label='Info', default=user_form.info),
                           submit_button = T('Update Info'),
                           )
    if form.process().accepted:
        user.info = form.vars.info
        redirect(URL('users', 'index'))
    # p.name would contain the name of the poster.
    return dict(form=form, user=user_form)

@auth.requires_login()
def send_message():
    user = db(db.auth_user.username == request.args(0)).select().first() or redirect('users', 'index')
    
    sender = auth.user.username
    reciever = user.username
    form = SQLFORM.factory(Field('reciever', label='To', default=user.username, writable=False),
                           Field('subject', label='Subject', default=''),
                           Field('info', 'text', label='Info',),
                           submit_button = T('Send Message'),
                           )
    if form.process().accepted:
        db.messages.insert(sender=sender,
                            reciever=reciever,
                            subject=form.vars.subject,
                            mess_type = 'Personal',
                            body=form.vars.info,
                            )
        redirect(URL('users', 'index'))
    return dict(form=form)

@auth.requires_login()
def add_friend():
    user = db(db.auth_user.username == request.args(0)).select().first() or redirect('users', 'index')
    
    sender = auth.user.username
    reciever = user.username
    form = SQLFORM.factory(Field('reciever', label='To', default=user.username, writable=False),
                           Field('subject', label='Subject', default='New Friend Request'),
                           Field('info', 'text', label='Info',),
                           submit_button = T('Send Friend request'),
                           )
    if form.process().accepted:
        db.messages.insert(sender=sender,
                            reciever=reciever,
                            subject=form.vars.subject,
                            mess_type = 'Friend Request',
                            body=form.vars.info,
                            )
        redirect(URL('users', 'index'))
    return dict(form=form)
