#  __author__ = 'Alexey Buchkin'

import pymysql.cursors
from model.project import Project


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_project_list(self):
        cursor = self.connection.cursor()
        list = []
        try:
            cursor.execute("select id, name, status, view_state, description, inherit_global from mantis_project_table")
            for row in cursor:
                (id, name, status, view_state, description, inherit_global) = row
                list.append(Project(id=str(id), name=name, status=self.modification_status(status),
                                    view_state = self.modification_view_state(view_state),
                                    description=description,
                                    inherit_global=self.modification_inherit_global(inherit_global)))
        finally:
            cursor.close()
        return list

    def modification_inherit_global(self, text):
        unit_to_multiplier = {
            '1': 'True',
            '0': 'False'
        }
        return unit_to_multiplier[str(text)]

    def modification_status(self, text):
        unit_to_multiplier = {
            '10': 'в разработке',
            '30': 'выпущен',
            '50': 'стабильный',
            '70': 'устарел'
        }
        return unit_to_multiplier[str(text)]

    def modification_view_state(self, text):
        unit_to_multiplier = {
            '10': 'публичный',
            '50': 'приватный'
        }
        return unit_to_multiplier[str(text)]

    def delete_project(self, project):
        cursor = self.connection.cursor()
        try:
            cursor.execute("delete from mantis_project_table where id = %s" % project.id)
        finally:
            cursor.close()
        return


    def destroy(self):
        self.connection.close()
