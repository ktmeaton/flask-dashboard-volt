from app.api import blueprint
from app import db
from flask_restful import Resource, Api, reqparse

# from flask_login import login_required, current_user

# from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)
# from app.base.models import User
from app.home.models import Workflow

api = Api(blueprint)


class WorkflowListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "system1",
            type=str,
            required=True,
            help="No system provided",
            location="json",
        )
        self.reqparse.add_argument("node1", type=str, location="json")
        super(WorkflowListAPI, self).__init__()

    def get(self):
        # Retrieve workflows from the database
        workflows = (
            db.session.query(Workflow)
            # .filter(Workflow.username == str(current_user))
            .all()
        )
        # Convert to dictionary format for json
        for i in range(0, len(workflows)):
            workflows[i] = workflows[i].as_dict()
        return workflows

    def post(self):
        pass


class WorkflowAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "system", type=str, location="json", help="No system provided"
        )
        super(WorkflowAPI, self).__init__()

    def get(self, id):
        workflow = db.session.query(Workflow).filter(Workflow.id == id).first()
        if workflow:
            workflow = workflow.as_dict()
            return workflow, 200
        else:
            return 404


api.add_resource(WorkflowListAPI, "/api/v0.1.0/workflows", endpoint="workflows")
api.add_resource(WorkflowAPI, "/api/v0.1.0/workflows/<int:id>", endpoint="workflow")
