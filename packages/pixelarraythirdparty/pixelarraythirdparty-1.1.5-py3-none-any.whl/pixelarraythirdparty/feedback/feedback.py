from pixelarraythirdparty.client import AsyncClient


class FeedbackManagerAsync(AsyncClient):
    async def create_feedback(
        self,
        project_id: int,
        content: str,
        contact_info: str,
    ):
        """
        description:
            创建新的客户反馈，反馈必须关联一个项目。
        parameters:
            project_id(int): 项目ID，必须关联一个已存在的项目
            content(str): 反馈内容
            contact_info(str): 反馈人联系方式
        return:
            data(dict): 反馈信息
                - id(int): 反馈ID
                - project_id(int): 项目ID
                - content(str): 反馈内容
                - contact_info(str): 反馈人联系方式
                - created_at(str): 反馈创建时间
            success(bool): 操作是否成功
        """
        data = {
            "project_id": project_id,
            "content": content,
            "contact_info": contact_info,
        }
        data, success = await self._request("POST", "/api/feedback/create", json=data)
        if not success:
            return {}, False
        return data, True

    async def list_feedback(
        self,
        page: int = 1,
        page_size: int = 10,
        project_id: int = None,
    ):
        """
        description:
            分页查询反馈列表，支持按项目ID进行筛选。
        parameters:
            page(int): 页码
            page_size(int): 每页数量
            project_id(int): 项目ID筛选，可选
        return:
            data(dict): 反馈列表信息
                - feedbacks(list): 反馈列表
                    - id(int): 反馈ID
                    - project_id(int): 项目ID
                    - project_name(str): 项目名称
                    - content(str): 反馈内容
                    - contact_info(str): 反馈人联系方式
                    - created_at(str): 反馈创建时间
                - total(int): 总反馈数量
                - page(int): 当前页码
                - page_size(int): 每页数量
            success(bool): 操作是否成功
        """
        params = {
            "page": page,
            "page_size": page_size,
        }
        if project_id is not None:
            params["project_id"] = project_id
        data, success = await self._request("GET", "/api/feedback/list", params=params)
        if not success:
            return {}, False
        return data, True

    async def get_feedback_detail(self, feedback_id: int):
        """
        description:
            根据反馈ID获取反馈的详细信息。
        parameters:
            feedback_id(int): 反馈ID
        return:
            data(dict): 反馈详细信息
                - id(int): 反馈ID
                - project_id(int): 项目ID
                - project_name(str): 项目名称
                - content(str): 反馈内容
                - contact_info(str): 反馈人联系方式
                - created_at(str): 反馈创建时间
            success(bool): 操作是否成功
        """
        data, success = await self._request("GET", f"/api/feedback/{feedback_id}")
        if not success:
            return {}, False
        return data, True

    async def delete_feedback(self, feedback_id: int):
        """
        description:
            根据反馈ID删除指定的反馈记录。仅管理员可删除反馈。
        parameters:
            feedback_id(int): 反馈ID
        return:
            data(None): 删除成功时返回None
            success(bool): 操作是否成功
        """
        data, success = await self._request("DELETE", f"/api/feedback/{feedback_id}")
        if not success:
            return {}, False
        return data, True

