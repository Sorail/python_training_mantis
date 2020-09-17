from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password, config):
        client = Client(config["web"]["baseUrl"] + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def project_list(self, username, password, config):
        client = Client(config["web"]["baseUrl"] + "/api/soap/mantisconnect.php?wsdl")
        try:
            list = client.service.mc_projects_get_user_accessible(username, password)
            result = []
            for p in list:
                result.append(Project(id=p['id'], name=p['name'], status=p['status']['name'],
                                      view_state=p['view_state']['name'], description=p['description']))
            return result
        except WebFault:
            return None
