# Python imports

# Framework imports

# Local imports
from datetime import datetime, timedelta
from gwBackend.generic.controllers import Controller
from gwBackend.LeadsManagement.models.FollowUp import FollowUp
from gwBackend.LeadsManagement.models.Lead import Leads
from gwBackend.UserManagement.controllers.UserController import UserController
# from gwBackend.LeadsManagement.controllers.LeadsController import LeadsController
from gwBackend.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from gwBackend import config


class FollowUpController(Controller):
    Model = FollowUp

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages, data = cls.cls_validate_data(data=data,
                                                               return_data=True)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        # if common_utils.get_time() > common_utils.convert_to_epoch(data[constants.FOLLOW_UP__NEXT]):
        #     return response_utils.get_response_object(
        #         response_code=response_codes.CODE_WRONG_PARAMETERS,
        #         response_message=response_codes.MESSAGE_HAS_TO_BE_LESS_THAN.format(
        #             constants.FOLLOW_UP__NEXT, constants.CURRENT_TIME
        #         ))
        # if data[constants.FOLLOW_UP__LEAD][constants.CREATED_BY] != common_utils.current_user():
        #     return response_utils.get_response_object(
        #         response_code=response_codes.CODE_UNAUTHENTICATED_ACCESS,
        #         response_message=response_codes.MESSAGE_UNAUTHENTICATED_ACCESS
        #     )
        # data[constants.FOLLOW_UP__LEAD][constants.LEAD__STATUS] = data[constants.FOLLOW_UP__STATUS]
        # data[constants.FOLLOW_UP__LEAD].save()
        _, _, obj = cls.db_insert_record(data=data)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        filter = {}
        filter_data = {**data}
        filter_fields = {
            "project":constants.PROJECT,
            "level": constants.LEAD__LEVEL__LIST,
            "Task": constants.FOLLOW_UP__TYPE_LIST,
            "Team": [],
        }
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.FOLLOW_UP__NEXT_DEADLINE +
                   "__gte"] = datetime.strptime(datefrom, config.FILTER_DATETIME_FORMAT)
            filter[constants.FOLLOW_UP__NEXT_DEADLINE +
                   "__lte"] = datetime.strptime(dateto, config.FILTER_DATETIME_FORMAT)
        
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
            filter_data['assigned_to_name'] = user_childs[0]['name']
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

        if data.get('Task'):
            filter[constants.LEAD__FOLLOWUP_TYPE] = data.get('Task')
        
        if data.get(constants.LEAD__LEVEL):
            filter[constants.LEAD__LEVEL] = data.get(constants.LEAD__LEVEL)

        if data.get(constants.LEAD__PROJECT):
            filter[constants.LEAD__PROJECT] = data.get(constants.LEAD__PROJECT)
        
        if data.get('last_work'):
            filter[constants.LEAD__LAST_WORK_DATE + "__lte"] =  common_utils.convert_to_epoch1000(data.get('last_work'), format=config.DATETIME_FORMAT)

        if data.get('page'):
            page = int(data['page'])
        else:
            page = 1
        
        if data.get('per_page'):
            per_page = int(data('per_page'))
        else:
            per_page = 50

        if data.get('client_name'):
            filter[constants.LEAD__FIRST_NAME + '__in'] = data.get('client_name')

        if data.get('lead_id'):
            filter[constants.LEAD__ID] = data.get('lead_id')

        if data.get('phone_number'):
            filter[constants.LEAD__PHONE_NUMBER] = data.get('phone_number')

        if data.get('day'):
            filter_day = data.get('day')
        else:
            filter_day = 'overdue'

        user_ids = [str(id[constants.ID]) for id in user_childs]
        filter[constants.FOLLOW_UP__ASSIGNED_TO+"__in"] = user_ids

        followup_dataset = []
        followup_data = {}
        overdue = []
        today = []
        tomorrow = []
        next7 = []
        all = []

        queryset = cls.db_read_records(
            read_filter={**filter}).aggregate(pipeline.LAST_FOLLOWUP)
        followup_dataset = [obj for obj in queryset]
        # temp = {obj['_id']:{'data':obj} for obj in queryset}
        # lead_id = [temp[obj]['data']['_id'] for obj in temp]
        # from gwBackend.LeadsManagement.controllers.LeadsController import LeadsController
        # lead_data = LeadsController.read_lead_min(lead_id)
        # for obj in lead_data:
        #     temp[obj['id']].update({'lead':obj})

        for item in followup_dataset:
            # print(datetime.now().date())
            # print(item['data']['next_deadline'].date())
            now = datetime.utcnow().date()
            if item['deadline'].date() < now:
                overdue.append(item)
            if item['deadline'].date() == now:
                today.append(item)
            if item['deadline'].date() == (now + timedelta(days=1)):
                tomorrow.append(item)
            if item['deadline'].date() > now and item['deadline'].date() <= (now + timedelta(days=7)):
                next7.append(item)
            all.append(item)
        # followup_dataset.append([user.name, tmp, tmp_follow])

            # for obj in queryset:
            #     tmp = obj.display()
            #     # tmp['followup'] = FollowUpController.read_count(tmp['id'])
            #     lead_data.append(FollowUpController.read_count(['id']))
            # lead_dataset.append(
            #     [str(user.pk), user[constants.USER__NAME], lead_data])
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        # followup_data['followup'] = followup_dataset

        followup_data = {}
        followup_data['overdue'] = overdue
        followup_data['today'] = today
        followup_data['tomorrow'] = tomorrow
        followup_data['next7'] = next7
        followup_data['all'] = all
        
        followup_data['usernamne'] = common_utils.current_user()[
            constants.USER__NAME]
        followup_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        followup_data['userlevel'] = common_utils.current_user()[
            constants.USER__ROLE][constants.USER__ROLE__ROLE_ID]
        followup_data['all_users'] = all_users
        # followup_data['pagination'] = {
        #     "next_num": queryset.next_num,
        #     "page": queryset.page,
        #     "pages": queryset.pages,
        #     "per_page": queryset.per_page,
        #     "prev_num": queryset.prev_num,
        #     "total": queryset.total,
        #     "has_next": queryset.has_next,
        #     "has_prev": queryset.has_prev
        # }
        # followup_data['filter_fields'] = filter_fields
        # followup_data['filter_data'] = filter_data
        # followup_dataset.append(user.name)
        followup_data['data'] = ''
        followup_data['pagination'] = ''
        followup_data['filter_fields'] = filter_fields
        followup_data['filter_data'] = filter_data
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=followup_data
        )

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
                    constants.FOLLOW_UP.title(), constants.ID
                ))
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )

    @classmethod
    def read_count(cls, lead_id):
        queryset = cls.db_read_records(
            read_filter={constants.FOLLOW_UP__LEAD: lead_id})
        followup = {'count': queryset.count()}
        followup['data'] = queryset.order_by(
            "-"+constants.CREATED_ON).first() or {}
        if followup["data"]:
            followup["data"] = followup["data"].display()
            # counter += 1
        return followup

    @classmethod
    def read_current_followup(cls, lead_id):
        queryset = cls.db_read_records(
            read_filter={constants.FOLLOW_UP__LEAD+"__in": lead_id}).aggregate(pipeline.LAST_FOLLOWUP)
        # followup = {'count': queryset.count()}
        # followup['data'] = queryset.order_by(
        #     "-"+constants.CREATED_ON).first() or {}
        # if followup["data"]:
        #     followup["data"] = followup["data"].display()
        temp = [obj for obj in queryset]
        return temp

    @classmethod
    def suspend_controller(cls, data):
        current_user = common_utils.current_user()
        filter = {}
        if current_user[constants.USER__ROLE] != constants.DEFAULT_ADMIN_ROLE_OBJECT:
            filter = {constants.CREATED_BY: current_user}
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID], **filter}, update_filter={
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
                constants.FOLLOW_UP.title(), constants.ID
            ))

    @classmethod
    def read_lead_follow(cls, data):
        queryset = cls.db_read_records(
            read_filter={constants.FOLLOW_UP__LEAD: data['lead']}).order_by("-created_on")
        followup_dataset = [obj.display() for obj in queryset]
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=[followup_dataset, data['name'], data['ref']]
        )
