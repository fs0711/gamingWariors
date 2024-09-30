# Python imports
from math import nan, isnan
# Framework imports
from flask_mongoengine import pagination
# Local imports
from ast import Constant
from gwBackend.generic.controllers import Controller
from gwBackend.OrganizationsManagement.models.Organization import Organization
from gwBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from gwBackend import config
from datetime import datetime, timedelta


class OrganizationController(Controller):
    Model = Organization


    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_json_response_object(
                            response_code=response_codes.CODE_VALIDATION_FAILED,
                            response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                            response_data=error_messages
                        )
    
        _,_,obj = cls.db_insert_record(data=data, db_commit=False)
        obj.save()
        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )


    @classmethod
    def read_controller(cls, data):
            return response_utils.get_json_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=[
                obj.display() for obj in cls.db_read_records(read_filter=data)
            ])


    @classmethod
    def update_controller(cls, data):
        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=data
        )
        if not is_valid:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.USER.title(), constants.ID
                ))
        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )


    @classmethod
    def suspend_controller(cls, data):
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]},
            update_filter={
                constants.STATUS: constants.OBJECT_STATUS_SUSPENDED},
            update_mode=constants.UPDATE_MODE__PARTIAL,
        )
        if obj:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.ORGANIZATION.title(), constants.ID
            ))


    @classmethod
    def get_organizations(cls):
        return response_utils.get_json_response_object(
        response_code=response_codes.CODE_SUCCESS,
        response_message=response_codes.MESSAGE_SUCCESS,
        response_data=[{'id':str(obj[constants.ID]),'organization_id':obj[constants.ORGANIZATION__ID], 'name':obj[constants.ORGANIZATION__NAME] ,'address':obj[constants.ORGANIZATION__ADDRESS],'cp_email_address':obj[constants.ORGANIZATION__CP_EMAIL], 'cp_phone_number':obj[constants.ORGANIZATION__CP_PHONE_NUMBER]}  for obj in cls.db_read_records(read_filter={})],
        )