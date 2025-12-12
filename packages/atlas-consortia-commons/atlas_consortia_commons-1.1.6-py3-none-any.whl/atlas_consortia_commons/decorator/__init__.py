import sys
import urllib.parse
from functools import wraps
from inspect import signature

from flask import current_app, request
from hubmap_commons.hm_auth import AuthHelper

from atlas_consortia_commons.rest import (
    abort_bad_req,
    abort_forbidden,
    abort_unauthorized,
)

if sys.version_info >= (3, 10):
    from dataclasses import dataclass

    @dataclass(slots=True, frozen=True)
    class User:
        uuid: str
        email: str
        group_uuids: list
        is_data_admin: bool

elif sys.version_info >= (3, 7):
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class User:
        uuid: str
        email: str
        group_uuids: list
        is_data_admin: bool

else:

    class User:
        def __init__(self, uuid, email, group_uuids, is_data_admin):
            self.uuid = uuid
            self.email = email
            self.group_uuids = group_uuids
            self.is_data_admin = is_data_admin


def require_json(
    param: str = "body",
):
    """A decorator that checks if the request content type is json.

    If a type hint is provided for the parameter, the basic request body type (dict or
    list) will be checked against the type hint. The content of the request body will
    not be validated further.

    If the decorated function has a parameter with the same name as `param`, the
    request body will be passed as that parameter.

    Parameters
    ----------
    param : str
        The name of the parameter to pass the request body to required.
        Defaults to "body".

    Example
    -------
        @app.route("/foo", methods=["POST"])
        @require_json(param="foo_body")
        def foo(foo_body: dict):
            return jsonify(foo_body)

        @app.route("/bar", methods=["PUT"])
        @require_json()
        def bar(body: dict):
            return jsonify(body)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                abort_bad_req("A json body and appropriate Content-Type header are required")

            if param and param in signature(f).parameters:
                # Check if the parameter has a type annotation
                p = signature(f).parameters[param]
                body = request.json
                if p.annotation is not p.empty and not isinstance(body, p.annotation):
                    abort_bad_req("Invalid json request body type")
                kwargs[param] = request.json

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_multipart_form(
    form_param: str = "form", files_param: str = "files", combined_param: str = "data"
):
    """A decorator that checks if the request content type is multipart/form-data.

    If the decorated function has a parameter with the same name as `form_param`, the
    form body will be passed as that parameter.

    If the decorated function has a parameter with the same name as `files_param`, the
    files will be passed as that parameter.

    If the decorated function has a parameter with the same name as `combined_param`,
    the form and files will be passed as that parameter.

    Parameters
    ----------
    form_param : str
        The name of the parameter to pass the form body.
        Defaults to "form".
    files_param : str
        The name of the parameter to pass the files.
        Defaults to "files".
    combined_param : str
        The name of the parameter to pass the form and files.
        Defaults to "data".

    Notes
    -----
    This decorator does not do any validation on the form request body.

    Example
    -------
        @app.route("/foo", methods=["POST"])
        @require_multipart_form(combined_param="foo_data")
        def foo(foo_data: dict):
            name = foo_data.get("name")
            return jsonify({"name": name})
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.content_type.startswith("multipart/form-data"):
                abort_bad_req("A form data body and appropriate Content-Type header are required")

            if form_param and form_param in signature(f).parameters:
                kwargs[form_param] = request.form

            if files_param and files_param in signature(f).parameters:
                kwargs[files_param] = request.files

            if combined_param and combined_param in signature(f).parameters:
                kwargs[combined_param] = request.values

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_data_admin(param: str = "token", user_param: str = "user"):
    """A decorator that checks if the user is a member of the SenNet Data Admin group.

    If the decorated function has a parameter with the same name as `param`, the
    user's token will be passed as that parameter. If the request has no token or an
    invalid token, a 401 Unauthorized response will be returned. If the user is not a
    member of the SenNet Data Admin group, a 403 Forbidden response will be returned.

    If the decorated function has a parameter with the same name as `user`, the
    user will be passed as that parameter. The `user` is of type `decorator.User`.

    Parameters
    ----------
    param : str
        The name of the parameter to pass the user's token to. Defaults to "token".
    user_param : str
        The name of the parameter to pass the user's information to. Defaults to "user".

    Example
    -------
        @app.route("/foo", methods=["POST"])
        @require_data_admin(param="foo_token")
        def foo(foo_token: str):
            return jsonify({"message": f"You are a data admin with token {foo_token}!"})

        @app.route("/bar", methods=["PUT"])
        @require_data_admin()
        def bar(token: str, user: User):
            return jsonify({"message": f"You are a data admin with token {token}!"})
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.headers.get("Authorization") is None:
                abort_unauthorized("User must supply a token")

            auth_helper = AuthHelper.configured_instance(
                current_app.config["APP_CLIENT_ID"],
                current_app.config["APP_CLIENT_SECRET"],
            )
            token = auth_helper.getUserTokenFromRequest(request, getGroups=True)
            if not isinstance(token, str):
                abort_unauthorized("User must be a member of the SenNet Consortium")

            is_data_admin = auth_helper.has_data_admin_privs(token)
            if is_data_admin is not True:
                abort_forbidden("User must be a member of the SenNet Data Admin group")

            if param and param in signature(f).parameters:
                kwargs[param] = token

            if user_param in signature(f).parameters:
                user_info = auth_helper.getUserInfo(token, getGroups=True)
                if not isinstance(user_info, dict):
                    abort_unauthorized("User must be a member of the SenNet Consortium")

                kwargs[user_param] = User(
                    uuid=user_info.get("sub"),
                    email=user_info.get("email"),
                    group_uuids=user_info.get("hmgroupids", []),
                    is_data_admin=is_data_admin is True,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_valid_token(param: str = "token", user_param: str = "user"):
    """A decorator that checks if the provided token is valid.

    If the decorated function has a parameter with the same name as `param`, the
    user's token will be passed as that parameter. If the request has no token or an
    invalid token, a 401 Unauthorized response will be returned.

    If the decorated function has a parameter with the same name as `user`, the
    user will be passed as that parameter. The `user` is of type `decorator.User`.

    Parameters
    ----------
    param : str
        The name of the parameter to pass the user's token to. Defaults to "token".
    user_param : str
        The name of the parameter to pass the user's information to. Defaults to "user".

    Example
    -------
        @app.route("/foo", methods=["POST"])
        @require_valid_token(param="foo_token", user_param="foo_user")
        def foo(foo_token: str, foo_user: User):
            return jsonify({
                "message": (
                    f"You are a valid user with token {foo_token} "
                    f"and groups {user.group_uuids}!"
                )
            })

        @app.route("/bar", methods=["PUT"])
        @require_valid_token()
        def bar(token: str):
            return jsonify({"message": f"You are a valid user with token {token}!"})
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.headers.get("Authorization") is None:
                abort_unauthorized("User must supply a token")

            auth_helper = AuthHelper.configured_instance(
                current_app.config["APP_CLIENT_ID"],
                current_app.config["APP_CLIENT_SECRET"],
            )

            token = auth_helper.getUserTokenFromRequest(request, getGroups=True)
            if not isinstance(token, str):
                print("Token is not a string")
                abort_unauthorized("User must be a member of the SenNet Consortium")

            user_info = auth_helper.getUserInfo(token, getGroups=True)
            if not isinstance(user_info, dict):
                print("User info is not a dict")
                abort_unauthorized("User must be a member of the SenNet Consortium")

            if param in signature(f).parameters:
                kwargs[param] = token

            if user_param in signature(f).parameters:
                is_admin = auth_helper.has_data_admin_privs(token)
                kwargs[user_param] = User(
                    uuid=user_info.get("sub"),
                    email=user_info.get("email"),
                    group_uuids=user_info.get("hmgroupids", []),
                    is_data_admin=isinstance(is_admin, bool) and is_admin is True,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def strip_whitespace_id():
    """A decorator that strips whitespace from the ID in a path variable.

    Example
    -------
        @app.route("/foo/<id>", methods=["GET"])
        @strip_whitespace_id
        def foo(id: str):

    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "id" in kwargs:
                original_id = kwargs["id"]
                # URL decode the ID and strip any whitespace
                kwargs["id"] = urllib.parse.unquote(original_id).strip()
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def suppress_reindex(param: str = "reindex"):
    """A decorator that checks if reindexing should be suppressed. Default to reindexing in all
    other cases.

    Parameters
    ----------
    param : str
        The name of the parameter to pass whether or not to reindex. Defaults to "reindex".

    Example
    -------
        @app.route("/foo", methods=["POST"])
        @suppress_reindex(reindex="foo_reindex")
        def foo(foo_reindex: str):
             if suppress_reindex:
                logger.log(level=logging.INFO
                , msg=f"Re-indexing suppressed during modification of {normalized_entity_type}"
                f" with UUID {entity_uuid}")
            else:
                reindex_entity(entity_uuid, user_token)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "reindex" not in request.args:
                kwargs["suppress_reindex"] = False
                return f(*args, **kwargs)

            reindex_str = request.args.get("reindex").lower()
            if reindex_str == "false":
                kwargs["suppress_reindex"] = True
                return f(*args, **kwargs)
            elif reindex_str == "true":
                kwargs["suppress_reindex"] = False
                return f(*args, **kwargs)
            raise Exception(
                f"The value of the 'reindex' parameter must be True or False (case-insensitive)."
                f" '{request.args.get('reindex')}' is not recognized."
            )

        return decorated_function

    return decorator
