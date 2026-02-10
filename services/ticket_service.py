from session_manager import SessionManager
from requests import Response
from models import SearchParams


class TicketService:
    """负责车票查询相关接口"""
    
    @classmethod
    def search_tickets(clazz, params):
        """查询车票信息
        
        Args:
            params: 查询参数，可以是 SearchParams 实例或字典
        
        Returns:
            车票查询结果的 JSON 数据
        """
        # 如果是 SearchParams 实例，获取其参数字典
        if isinstance(params, SearchParams):
            params = params.get_params()
        response: Response = SessionManager.get_session().get(url='https://kyfw.12306.cn/otn/leftTicket/queryG', params = params)
        return response.json()
