from requests.sessions import Session

from session_manager import SessionManager
from requests.models import Response


class TicketService:
    """负责车票查询相关接口"""    
    
    @classmethod
    def search_tickets(clazz):

        session: Session = SessionManager.get_session()
        
        params = {
            'leftTicketDTO.train_date': '2026-02-15',
            'leftTicketDTO.from_station': 'BJP',
            'leftTicketDTO.to_station': 'SHH',
            'purpose_codes': 'ADULT'
        }
        
        response: Response = session.get(url='https://kyfw.12306.cn/otn/leftTicket/queryG', params=params)
        return response.json()
