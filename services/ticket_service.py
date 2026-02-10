from session_manager import SessionManager
from requests import Response
from models import SearchParams
from models import SearchResult


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
        try:
            arr = []
            results = response.json()['data']['result']
            for result in results:
                item = []
                search_result = SearchResult(result)
                item.append(search_result.decryptField())
                item.append(search_result.getTrainNo())
                item.append(search_result.getStartStation())
                item.append(search_result.getEndStation())
                item.append(search_result.getFromStation())
                item.append(search_result.getToStation())
                item.append(search_result.getDepartureTime())
                item.append(search_result.getArrivalTime())
                item.append(search_result.getDuration())
                arr.append(item)
            return arr
        except:
            SessionManager.clear_session()
            return 'fail'
        
        
