# Python imports
import os
# Framework imports
from flask import Blueprint, request

# Local imports
from gwBackend.generic.services.utils import constants, decorators, common_utils
from gwBackend.BranchManagement.controllers.BranchController import BranchController
from gwBackend.config import config

branch_bp = Blueprint("branch_bp", __name__)


@branch_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__BRANCH,
    constants.OPTIONAL_FIELDS_LIST__BRANCH,
    request_form_data=False
)
def branch_create_view(data):
    res = BranchController.create_controller(data=data)
    return res


@branch_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN, constants.ROLE_ID_OWNER, constants.ROLE_ID_CLIENT])
@decorators.keys_validator()
def read_view(data):
    res = BranchController.read_controller(data=data)
    return res


@branch_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__BRANCH,
)
def update_view(data):
    return BranchController.update_controller(data=data)


@branch_bp.route("/search", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator()
def search_view(data):
    data = request.form
    res = BranchController.search_controller(data=data)
    return res

@branch_bp.route("/suspend", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [constants.ID]
)
def suspend_view(data):
    data = common_utils.posted()
    res = BranchController.suspend_controller(data=data)
    return res


@branch_bp.route("/list_branchs", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([])
@decorators.keys_validator()
def list_view(data):
    return BranchController.get_branchs()

@branch_bp.route("/list_branchs_ids", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([])
@decorators.keys_validator()
def list_view_ids(data):
    return BranchController.get_branchs_ids()

@branch_bp.route("/list_by_orgs", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN,constants.ROLE_ID_OWNER, constants.ROLE_ID_CLIENT])
@decorators.keys_validator(
    [constants.BRANCH__ORGANIZATION]
)
def list_branchs_by_orgs(data):
    res = BranchController.get_branchs_orgs(data=data)
    return res