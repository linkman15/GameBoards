# -*- coding: utf-8 -*-
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    return dict(message=T('Welcome to Game Boards.'))
