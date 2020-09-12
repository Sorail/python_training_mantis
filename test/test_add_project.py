# -*- coding: utf-8 -*-
#  __author__ = 'Alexey Buchkin'

from model.project import Project


def test_add_group(app):
    app.project.open_project_page()
    project = Project(name='New Project 1')
    app.project.create(project)
