# -*- coding: utf-8 -*-
# try something like
def index(): 
    q = db.games

    def generate_view_button(row):
        # Views the post
        b = A('View', _class='btn', _href=URL('game_list', 'view', args=[row.id]))
        return b
    
    def generate_add_button(row):
        # Views the post
        b = A('Add to Profile', _class='btn', _href=URL('game_list', 'add', args=[row.id]))
        return b
    
    links = [
        dict(header='', body = generate_view_button),
        dict(header='', body = generate_add_button),
    ]
    
    start_idx = 0
    
    form = SQLFORM.grid(q, args=request.args[:start_idx],
                        fields=[db.games.name],
        editable=False, deletable=False, details = False, 
        csv = False,
        create=False,
        links=links,
        paginate=50,
        )
    
    return dict(form=form)

def view():
    """View game."""
    p = db.games(request.args(0)) or redirect(URL('default', 'index'))
    form = SQLFORM(db.games, record=p, readonly=True)
    # p.name would contain the name of the poster.
    return dict(form=form, games = p)

def add():
    form = FORM.confirm('Yes',{'No':URL('game_list', 'index')})
    game_add = db.games(request.args(0))
    #current_games = auth.user.games
    if form.accepted:
        user = db(db.auth_user.username == auth.user.username).select().first()
        user.update_record(games=user.games+[game_add])
        redirect(URL('game_list', 'index'))
    return dict(form=form)
