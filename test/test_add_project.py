# -*- coding: utf-8 -*-
#  __author__ = 'Alexey Buchkin'

from model.project import Project


def test_add_group(app, db):
    project = Project(name='New Project 1', inherit_global=True)
    app.project.open_project_page()
    old_projects = db.get_project_list()
    for p in old_projects:
        if p.name == project.name:
            db.delete_project(p)
            old_projects.remove(p)
    app.project.create(project)
    new_projects = db.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
