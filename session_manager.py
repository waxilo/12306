import requests
from requests.sessions import Session


class SessionManager:

    _session: Session | None = None
    
    @classmethod
    def get_session(cls) -> Session:

        if cls._session is None:
            cls._session = requests.Session()
            cls._session.get("https://www.12306.cn/index/otn/login/conf")
        return cls._session


