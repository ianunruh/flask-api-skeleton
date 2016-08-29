from functools import wraps
import math

from flask import Response, g, jsonify, request

from backend.app import app
from backend.model import Session, User


@app.errorhandler(Exception)
def handle_exception(ex):
    app.logger.exception(ex)
    return make_error_response('Internal server error', 500)


@app.before_request
def check_auth():
    session = None
    user = None

    token = request.headers.get('X-Auth-Token')
    if token:
        session = Session.query.filter_by(token=token).first()
        if not session:
            return make_error_response('Invalid session token', 401)

        user = session.user
    else:
        auth = request.authorization
        if auth:
            user = User.find_by_email_or_username(auth.username)
            if not (user and user.password == auth.password):
                return make_error_response('Invalid username/password combination', 401)

    g.current_session = session
    g.current_user = user


def make_error_response(message, status_code=400, **kwargs):
    response = jsonify(message=message, **kwargs)
    response.status_code = status_code

    return response


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.current_user:
            return make_error_response('Auth token required', 403)

        return f(*args, **kwargs)

    return wrapper


def inject_context(context):
    ctx = {}
    if context:
        ctx.update(context)

    ctx['current_user'] = g.current_user
    return ctx


def dump_with_schema(schema_cls, many=False, paged=False,
                     context=None, status_code=None,
                     default_per_page=30, max_per_page=100,
                     **schema_kwargs):
    def outer(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, Response):
                return result

            schema = schema_cls(many=(many or paged), context=inject_context(context), **schema_kwargs)

            if paged:
                # result should be an SQLAlchemy query
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', default_per_page))
                if per_page > max_per_page:
                    return make_error_response('Exceeded max per page limit', 400)

                count = result.count()
                items = result.offset((page - 1) * per_page).limit(per_page)

                data = {
                    'items': schema.dump(items).data,
                    'count': count,
                    'page': page,
                    'per_page': per_page,
                    'total_pages': math.ceil(count / per_page),
                }

            data = schema.dump(result).data

            response = jsonify(data)

            if status_code:
                response.status_code = status_code

            return response

        return wrapper

    return outer


def load_with_schema(schema_cls, **schema_kwargs):
    def outer(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            schema = schema_cls(**schema_kwargs)
            json = request.get_json(force=True)
            data, errors = schema.load(json)
            if errors:
                return make_error_response('Validation failed', errors=errors, status_code=422)

            return f(data=data, *args, **kwargs)

        return wrapper

    return outer

from backend.routes import sessions, user # noqa
