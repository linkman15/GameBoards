# -*- coding: utf-8 -*-
# try something like
def index(): 
    board_group = request.args(0)
    
    p = db.gameboard.board_type == board_group
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = ''
        #if auth.user == row.poster:
        b = A('Delete', _class='btn', _href=URL('posts', 'delete_item', args=[row.id]))
        return b
    
    def generate_edit_button(row):
        # If the record is ours, we can delete it.
        b = ''
        #if auth.user_id == row.user_id:
        #    b = A('Edit', _class='btn', _href=URL('default', 'edit', args=[row.id]))
        return b
    
    def generate_view_button(row):
        # Views the post
        b = A('View', _class='btn', _href=URL('posts', 'view', args=[row.id]))
        return b
    
    links = [
        dict(header='', body = generate_view_button),
        dict(header='', body = generate_del_button),
        dict(header='', body = generate_edit_button),
        ]
    
    form = SQLFORM.grid(p, args=request.args[:0],
                        fields=[db.gameboard.subject,  db.gameboard.poster, ],
        editable=False, deletable=False, details = False, 
        csv = False,
        create = False,
        user_signature=False,
        links=links,
        paginate=25,
        )
    
    return dict(form=form, group=board_group)

def group():
    g = db(db.game_group.group_name == request.args(0)).select().first()
    
    p = db.gameboard.board_type == g.id
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = ''
        #if auth.user == row.poster:
        b = A('Delete', _class='btn', _href=URL('posts', 'delete_item', args=[row.id],))
        return b
    
    def generate_edit_button(row):
        # If the record is ours, we can delete it.
        b = ''
        #if auth.user_id == row.user_id:
            #b = A('Edit', _class='btn', _href=URL('default', 'edit', args=[row.id]))
        return b
    
    def generate_view_button(row):
        # Views the post
        #b = A('View', _class='btn', _href=URL('default', 'view', args=[row.id]))
        return b
    
    links = [
        dict(header='', body = generate_view_button),
        dict(header='', body = generate_del_button),
        dict(header='', body = generate_edit_button),
        ]
    
    form = SQLFORM.grid(p, args=request.args[:0],
                        fields=[db.gameboard.subject, db.gameboard.poster, ],
        editable=False, deletable=False, details = False, 
        csv = False,
        links=links,
        paginate=25,
        )
    
    return dict(form=form, )

def view():
    p = db.gameboard(request.args(0)) or redirect(URL('posts', 'index'))
    #name = p.group_name
    form = SQLFORM(db.gameboard,record=p, readonly=True)
    #members = p.members
    #owner = p.owner
    #mods = p.moderators
    return dict(form=form, poster=form.vars.poster, group=form.vars.board_type)

@auth.requires_login()
def add():
    #games = []
    group = request.args(0)
    poster=auth.user.username
    form = SQLFORM.factory(#Field('poster', label='Poster', default=auth.user.username, writable=False),
                   Field('subject',label='Subject',),
                   Field('games',label='Game', requires = IS_IN_DB(db, db.games, '%(name)s')),
                   Field('info', 'text'),
                   )
    #games = []
    #game_form = SQLFORM.factory(Field('add_games',label='Add Game', requires = IS_IN_DB(db, db.games, '%(name)s')), 
                                #submit_button = T('Add'))
    #if game_form.process().accepted:
        #games.extend(game_form.vars.add_games)
    
    if form.process().accepted:
       db.gameboard.insert(poster=poster,
                           subject=form.vars.subject,
                           game=form.vars.games,
                           board_type=group,
                           body=form.vars.info,
                           )
       #db.gameboard.truncate()
       redirect(URL('posts', 'index', args=group))
    return dict(form=form,)

@auth.requires_login()
def delete_item():
    p = db.gameboard(request.args(0)) or redirect(URL('posts', 'index', args='general'))
    #if p.user_id != auth.user_id:
        #session.flash = T('Not authorized.')
        #redirect(URL('posts', 'index', args='general'))
    db(db.gameboard.id == p.id).delete()
    redirect(URL('posts', 'index', args='general'))
