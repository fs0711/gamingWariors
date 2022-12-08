# Date Created 14/09/2021 17:05:00


# Local imports
from gwBackend import app
from gwBackend.LeadsManagement.controllers.LeadsController import LeadsController
from gwBackend.LeadsManagement.controllers.FollowUpController import FollowUpController
from gwBackend.LeadsManagement.controllers.LeadsHistoryController import LeadsHistoryController
from gwBackend.generic.services.utils import constants, pipeline
import re


def junk_follow_up_lead_history_removal(run=True):
    if not run:
        return
    with app.test_request_context():
        # followUps = FollowUpController.db_read_records(read_filter={
        #     constants.FOLLOW_UP__ASSIGNED_TO: '619b5af5a30ed6b97330addf'})
        # # followUps = followUps.aggregate([
        # #     {
        # #         '$group': {
        # #             '_id': '$lead',
        # #             'all_id': {
        # #                 '$addToSet': '$_id'
        # #             }
        # #         }
        # #     }ObjectId('62e24df0400954ae11bc1dee')
        # # ])
        # # followupss = list(followUps)
        # for follow in followUps:
        #     lead = LeadsController.db_read_single_record(read_filter={constants.ID: follow[constants.FOLLOW_UP__LEAD].fetch().id})
        #     res = FollowUpController.db_update_single_record(read_filter={constants.ID: follow[constants.ID]}, update_filter={constants.ID: follow[constants.ID], 
        #     constants.FOLLOW_UP__ASSIGNED_TO: lead[constants.LEAD__ASSIGNED_TO].fetch().id})
        #     print(res)
        # # del_followUp = []
        # # for follow in followupss:
        # #     del_followUp.extend(follow["all_id"])
        # # print("del_followUp", del_followUp)
        # # followaUps = "[ObjectId('" + "'),ObjectId('".join(map(str, del_followUp)) + "')]"
        # # print("del_followUp", followaUps)

        # leadGroups = LeadsHistoryController.db_read_records(read_filter={}).aggregate([
        #     {
        #         '$group': {
        #             '_id': '$lead_id',
        #             'all_id': {
        #                 '$addToSet': '$_id'
        #             }
        #         }
        #     }
        # ])
        # leads = list(leadGroups)
        # del_history = []
        # for leadGroup in leads:
        #     del_history.extend(leadGroup["all_id"][1:])
        # string = "[ObjectId('" + \
        #     "'),ObjectId('".join(map(str, del_history)) + "')]"
        # print("string", string)


        data = {}
        count = 0
        data['transfer_to'] = '6253cce240d74a484aff4cd9'
        leadh = LeadsController.db_read_records(read_filter={"phone_number":re.compile('^\+920')})
        for lead in leadh:
            number = lead['phone_number'][0]
            number = re.sub('0','',number,1)
            # followup = FollowUpController.read_lead_follow(data = {'lead':lead['id'], 'name':'', 'ref':''})
            # total = len(followup['response_data'][0])
            # transfer_to = str(followup['response_data'][0][total-1][constants.CREATED_BY].fetch()[constants.ID])
            count +=1
            print(count)
            print(number)
            # data['transfer_to'] = followup['response_data'][0][0]['created_by']
            # for follow in followup['response_data'][0]:
            #     followup_updatedata = {constants.FOLLOW_UP__ASSIGNED_TO: data['transfer_to'],
            #     constants.ID: follow[constants.ID]}
            #     res = FollowUpController.update_controller(followup_updatedata)
            leads = {}
            # leads[constants.LEAD__FOLLOWUP] = res['response_data'][constants.ID]
            leads[constants.ID] = lead['id']
            # leads[constants.LEAD__COMMENT] = res['response_data'][constants.FOLLOW_UP__COMMENT]
            leads[constants.LEAD__LEVEL] = lead['lead_level']
            leads[constants.LEAD__PHONE_NUMBER] = [number]
            # leads[constants.LEAD__FOLLOWUP_COUNT] = total
            # leads[constants.LEAD__LAST_WORK] = res['response_data']['sub_type']
            # leads[constants.LEAD__LAST_WORK_DATE] = res['response_data']['created_on']
            # leads[constants.LEAD__FOLLOWUP_TYPE] = res['response_data']['type']
            # leads[constants.LEAD__FOLLOWUP_NEXT_DEADLINE] = res['response_data']['next_deadline']
            # leads[constants.LEAD__FOLLOWUP_NEXT_TASK] = res['response_data']['next_task']
            # leads[constants.LEAD__PROJECT] = res['response_data']['next_project']
            # leads[constants.LEAD__ASSIGNED_TO] = data['transfer_to']
            # leads[constants.LEAD__ASSIGNED_BY] = common_utils.current_user()
            # leads[constants.LEAD__TRANSFERED] = False
            # leads[constants.LEAD__TRANSFERED_ON] = common_utils.get_time()
            res = LeadsController.db_update_single_record(read_filter = {constants.ID:lead['id']}, update_filter = leads)
            print(res)