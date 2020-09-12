# -*- coding: utf-8 -*-
#  __author__ = 'Alexey Buchkin'

from model.project import Project
import random


def test_delete_group(app, db):
    app.project.open_project_page()
    if len(db.get_project_list()) == 0:
        app.project.create(Project(name='New Project 1'))

    old_projects = db.get_project_list()
    project = random.choice(old_projects)
    app.project.delete(project)
    new_projects = db.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects
