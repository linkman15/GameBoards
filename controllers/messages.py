# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index(): 
    messages = db.messages.reciever == auth.user.username
    
    def generate_view_button(row):
        # Views the group
        b = A('View', _class='btn', _href=URL('messages', 'view', args=[row.id]))
        return b
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = A('Delete', _class='btn', _href=URL('messages', 'delete_item', args=[row.id], user_signature=True))
        return b
    
    links = [
        dict(header='', body = generate_view_button),
        dict(header='', body = generate_del_button),
    ]
    
    form = SQLFORM.grid(messages,
                        fields=[db.messages.sender, db.messages.subject, db.messages.mess_type],
        editable=False, deletable=False, details = False, 
        csv = False,
        create = False,
        links=links,
        paginate=10,
        )
    
    return dict(form=form)

@auth.requires_login()
def view():
    message = db.messages(request.args(0)) or redirect(URL('messages', 'index'))
    form = ''
    if message.mess_type == 'Friend Request':
        form = FORM.confirm('Accept Request?')
        if form.accepted:
            sender = db(db.auth_user.username == message.sender).select().first()
            reciever = db(db.auth_user.username == message.reciever).select().first()
            sender.update_record(friends=sender.friends+[reciever])
            reciever.update_record(friends=reciever.friends+[sender])
            #reciever.friends.extend(sender)
    return dict(message=message, form=form)

@auth.requires_login()
def delete_item():
     item = db.messages(request.args(0)) or redirect(URL('messages', 'index'))
     form = FORM.confirm('Yes',{'No':URL('messages', 'index')})
     if form.accepted:
         db(db.messages.id == item.id).delete()
         redirect(URL('messages', 'index'))
     return dict(form=form)

def send_message():
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
                            mess_type = 'General',
                            body=form.vars.info,
                            )
        redirect('users', 'index')
    return dict(form=form)
