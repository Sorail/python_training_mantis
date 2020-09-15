# -*- coding: utf-8 -*-
#  __author__ = 'Alexey Buchkin'

from model.project import Project


def test_add_group(app, db, config):
    username = config['webadmin']['username']
    password = config['webadmin']['password']
    project = Project(name='New Project 1')
    old_projects = app.soap.project_list(username, password)
    app.project.open_project_page()
    for p in old_projects:
        if p.name == project.name:
            db.delete_project(p)
            old_projects.remove(p)
    app.project.create(project)
    new_projects = app.soap.project_list(username, password)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
