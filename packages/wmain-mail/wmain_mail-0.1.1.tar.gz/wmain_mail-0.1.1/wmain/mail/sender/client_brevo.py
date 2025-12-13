from typing import Tuple

from wmain.mail.sender.ports import MailSender
from wmain.core.http.api import Api, request


class BrevoHttpClient(Api, MailSender):

    def __init__(self, api_key: str) -> None:
        """

        :param api_key:
        """
        super().__init__(
            base_url="https://api.brevo.com/v3",
            headers={
                "accept": "application/json",
                "api-key": "{api_key}",
                "content-type": "application/json"
            }
        )
        self["api_key"] = api_key

    @request("get", "/v3/contacts/folders",
             params={
                 "limit": "{limit}",
                 "offset": "{offset}",
                 "sort": "{sort}"
             })
    async def get_all_folders(self,
                              limit: int = 50,
                              offset: int = 0,
                              sort: str = "desc"):
        """
        列出所有联系人文件夹
        """
        pass

    @request("get", "/v3/contacts/lists",
             params={
                 "limit": "{limit}",
                 "offset": "{offset}",
                 "sort": "{sort}",
             })
    async def get_all_lists(self,
                            limit: int = 50,
                            offset: int = 0,
                            sort: str = "desc"):
        """
        列出所有联系人列表
        """
        pass

    @request("get", "/v3/contacts/lists/{list_id}",
             params={
                 "startDate": "{start_date}",
                 "endDate": "{end_date}",
             })
    async def get_list_detail(self,
                              list_id: int,
                              start_date: str = "",
                              end_date: str = ""):
        """
        获取联系人列表
        :param: 格式必须是 YYYY-MM-DDTHH:mm:ss.SSSZ
        """
        pass

    @request("get", "/v3/contacts/lists/{list_id}/contacts",
             params={
                 "modifiedSince": "{modified_since}",
                 "limit": "{limit}",
                 "offset": "{offset}",
                 "sort": "{sort}",
             })
    async def get_list_contacts(self,
                                list_id: int,
                                modified_since: str = "",
                                limit: int = 50,
                                offset: int = 0,
                                sort: str = "desc"):
        """

        :param list_id: 列表的id
        :param modified_since: 格式 YYYY-MM-DDTHH:mm:ss.SSSZ
        :param limit:
        :param offset:
        :param sort:
        :return:
        """
        pass

    @request("post", "/v3/contacts",
             json={
                 "email": "{email}",
                 "listIds": "{list_ids}",
                 "updateEnabled": "{update_enabled}",
                 "attributes": "{attributes}",
                 "ext_id": "{ext_id}"
             })
    async def create_a_contact(self,
                               email: str,
                               ext_id: str = "",
                               list_ids: Tuple[int] = (),
                               update_enabled: bool = False,
                               attributes: dict = None):
        """
        添加联系人
        :param ext_id:
        :param attributes:
        :param email:
        :param list_ids:
        :param update_enabled:
        :return:
        """
        pass

    @request("get", "/v3/contacts/{identifier}",
             params={
                 "identifierType": "{identifier_type}",
                 "startDate": "{start_date}",
                 "endDate": "{end_date}",
             })
    async def get_a_contact_details(self,
                                    identifier: str,
                                    identifier_type: str = "email_id",
                                    start_date: str = "",
                                    end_date: str = ""):
        """
        获取联系人详情
        :param identifier:
        :param identifier_type: email_id
                                phone_id
                                contact_id
                                ext_id
                                whatsapp_id
                                landline_number_id
        :param start_date:
        :param end_date:
        :return:
        """
        pass

    @request("post", "/v3/events",
             json={
                 "event_name": "{event_name}",
                 "event_properties": "{event_properties}",
                 "identifiers": {
                     "ext_id": "{ext_id}",
                     "email_id": "{email_id}",
                 },
             })
    async def add_an_event(self,
                           event_name: str,
                           event_properties: dict = None,
                           ext_id: str = None,
                           email_id: str = None):
        """
        添加事件
        :param email_id:
        :param ext_id:
        :param event_name:
        :param event_properties:
        :return:
        """
        pass
