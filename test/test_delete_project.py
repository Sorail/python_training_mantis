# -*- coding: utf-8 -*-
#  __author__ = 'Alexey Buchkin'

from model.project import Project
import random


def test_delete_group(app, db, config):
    username = config['webadmin']['username']
    password = config['webadmin']['password']
    app.project.open_project_page()
    if len(app.soap.project_list(username, password)) == 0:
        app.project.create(Project(name='New Project 1'))

    old_projects = app.soap.project_list(username, password)
    project = random.choice(old_projects)
    app.project.delete(project)
    new_projects = app.soap.project_list(username, password)
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects
