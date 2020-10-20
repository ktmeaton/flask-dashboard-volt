from app.api import blueprint
from flask import jsonify
from flask_restful import Resource, Api
from flask_login import login_required, current_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.base.models import User
from app.home.models import Workflow

api = Api(blueprint)


class GetApiToken(Resource):
    @login_required
    def get(self):
        # expires = datetime.timedelta(days=7)
        # access_token = create_access_token(identity=str(current_user.id),
        # expires_delta=expires)
        access_token = create_access_token(identity=str(current_user.id))
        ret = {"access_token": access_token}
        return jsonify(ret)


# api.add_resource(TodoItem, '/todos/<int:id>')
api.add_resource(GetApiToken, "/api/token")


class APIWorkflowList(Resource):
    @jwt_required
    def get(self):
        jwt_user = get_jwt_identity()
        jwt_username = User.query.filter_by(id=jwt_user).first()
        workflows = Workflow.query.filter_by(username=str(jwt_username)).all()
        data = {}
        for workflow in workflows:
            data.update(workflow.as_dict())
        return jsonify(data)

    @jwt_required
    def post(self):
        print("TESTING")
        return jsonify({})


api.add_resource(APIWorkflowList, "/api/v0.1.0/workflows")


class APIWorkflow(Resource):
    @jwt_required
    def get(self, id):
        jwt_user = get_jwt_identity()
        jwt_username = User.query.filter_by(id=jwt_user).first()
        workflow = (
            Workflow.query.filter_by(username=str(jwt_username))
            .filter_by(id=id)
            .first()
        )
        if workflow:
            data = workflow.as_dict()
            return jsonify(data)
        else:
            return jsonify({})


api.add_resource(APIWorkflow, "/api/v0.1.0/workflows/<int:id>")
