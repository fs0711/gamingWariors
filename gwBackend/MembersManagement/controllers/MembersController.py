# Python imports

# Framework imports

# Local imports
from ast import Constant
from gwBackend.generic.controllers import Controller
from gwBackend.MembersManagement.models.Members import Members
from gwBackend.RfCardManagement.controllers.RfCardController import RfCardController
from gwBackend.generic.services.utils import constants, response_codes, response_utils, pipeline


class MembersController(Controller):
    Model = Members

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        # current_user = common_utils.current_user()
        already_exists = cls.db_read_records(read_filter={
            constants.MEMBER__PHONE_NUMBER+"__in": data[constants.MEMBER__PHONE_NUMBER],
            # constants.CREATED_BY+"__nin": [current_user]
        })
        if already_exists:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_USER_ALREADY_EXIST,
                response_message=response_codes.MESSAGE_ALREADY_EXISTS_DATA,
                response_data=already_exists
            )
        else:
            # card_id = data[constants.MEMBER__CARD_ID]
            # credit = data[constants.MEMBER__CREDIT]
            # del data[constants.MEMBER__CARD_ID]
            # del data[constants.MEMBER__CREDIT]
            is_valid,error_messages,objm = cls.db_insert_record(data=data)
            if is_valid:
                return response_utils.get_response_object(
                    response_code=response_codes.CODE_SUCCESS,
                    response_message=response_codes.MESSAGE_SUCCESS,
                    response_data=objm.display()
                )
            else: 
                return response_utils.get_response_object(
                    response_code=response_codes.CODE_CREATE_FAILED,
                    response_message=response_codes.MESSAGE_OPERATION_FAILED
                )

    @classmethod
    def read_controller(cls, data):
                return response_utils.get_response_object(
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
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.CLIENT.title(), constants.ID
                ))
        return response_utils.get_response_object(
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
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.MEMBER.title(), constants.ID
            ))
    

    
    # @classmethod
    # def card_charge_controller(cls, data):
    #     obj = cls.db_read_single_record(read_filter={
    #         constants.PROFILE__CARD_ID:data[constants.PROFILE__CARD_ID]})
    #     if obj[constants.PROFILE__CREDIT] - data[constants.GAMEUNIT__COST] >= 0:
    #         obj[constants.PROFILE__CREDIT] = obj[constants.PROFILE__CREDIT] - data[constants.GAMEUNIT__COST]
    #         obj.save()
    #         return {"status":1, "name":obj[constants.PROFILE__NAME], "balance":obj[constants.PROFILE__CREDIT]}
    #     else:
    #         return {"status":0, "name":obj[constants.PROFILE__NAME], "balance":obj[constants.PROFILE__CREDIT]}
    
    
    # @classmethod
    # def recharge_controller(cls, data):
    #     return
    
