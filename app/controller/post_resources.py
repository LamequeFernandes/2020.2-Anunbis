from flask_restful import Resource
from flask import request, make_response, jsonify
from ..schemas import post_schema
from ..services import post_services
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user
from ..model.student import Student
from ..ext.auth import student_required


class PostList(Resource):
    @student_required()
    def post(self):
        try:
            ps = post_schema.PostSchema(exclude=['id_post'])
            post = ps.load(request.json)
            if post.get('reg_student') != current_user.reg_student:
                raise ValidationError(
                    {'reg_student': 'Your reg_student is different to post.reg_student'})
            message, status_code = post_services.register_post(post)
            return make_response(jsonify(message), status_code)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
    
    @jwt_required()
    def get(self):
        reg_student = get_jwt_identity()
        student_post, status_code = post_services.post_student(reg_student)
        ps = post_schema.PostSchema(many=True)
        return make_response(ps.jsonify(student_post), status_code)



class PostAgreesList(Resource):
    @student_required()
    def post(self):
        try:
            student = current_user
            ps = post_schema.PostSchema(only=['id_post'])
            post_id = ps.load(request.json).get('id_post')
            post, status_code = post_services.agree_student_post(
                student, post_id)
            if status_code == 200:
                ps = post_schema.PostSchema(
                    context={'reg_student': student.reg_student})
                return make_response(ps.jsonify(post), status_code)
            else:
                return make_response(jsonify(post), status_code)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)


class PostDisagreesList(Resource):
    @student_required()
    def post(self):
        try:
            student = current_user
            ps = post_schema.PostSchema(only=['id_post'])
            post_id = ps.load(request.json).get('id_post')
            post, status_code = post_services.disagree_student_post(
                student, post_id)
            if status_code == 404:
                return make_response(jsonify(post), status_code)
            else:
                ps = post_schema.PostSchema(
                    context={'reg_student': student.reg_student})
                return make_response(ps.jsonify(post), status_code)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)





def configure(api):
    api.add_resource(PostList, "/post")
    api.add_resource(PostAgreesList, "/post/agree")
    api.add_resource(PostDisagreesList, "/post/disagree")