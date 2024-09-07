# Python imports
import os
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from gwBackend.OrganizationsManagement.controllers.organizationcontroller import OrganizationController
from gwBackend.generic.services.utils import constants, decorators, common_utils
from gwBackend.config import config

organizations_bp = Blueprint("organizations_bp", __name__)


@organizations_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
constants.REQUIRED_FIELDS_LIST__ORGANIZATION,
    constants.OPTIONAL_FIELDS_LIST__ORGANIZATION)
def create_organizations(data):
    res = OrganizationController.create_controller(data=data)
    return res


@organizations_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([])
@decorators.keys_validator()
def read_view(data):
    return OrganizationController.read_controller(data=data)


# @organizations_bp.route("/getorganizations", methods=["GET"])
# @decorators.is_authenticated
# @decorators.roles_allowed()
# # @decorators.keys_validator()
# def get_organizations():
#     res = OrganizationController.get_organizations()
#     return res


@organizations_bp.route("/update", methods=["GET","POST"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.UPDATE_FIELDS_LIST__ORGANIZATION,
    request_form_data=False
)
def update_view(data):
    if request.method == "POST":
        res = OrganizationController.update_controller(data=data)
        return res
    data = request.args
    res = OrganizationController.read_controller(data={constants.ID:data[constants.ID]})
    return render_template("editorganization.html", **res)


@organizations_bp.route("/suspend", methods=["GET"])
@decorators.is_authenticated
@decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [constants.ID],
    request_form_data=False
)
def suspend_view(data):
    res = OrganizationController.suspend_controller(data)
    return redirect("/api/organizations/read")


@organizations_bp.route("/list_organization", methods=["GET"])
@decorators.is_authenticated
# @decorators.roles_allowed([])
@decorators.keys_validator()
def list_view(data):
    return OrganizationController.get_organizations()