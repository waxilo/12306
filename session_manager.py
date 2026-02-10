import requests
from requests.sessions import Session
from fake_useragent import UserAgent


class SessionManager:

    _session: Session | None = None
    _ua: UserAgent | None = None

    
    @classmethod
    def get_session(cls) -> Session:

        if cls._session is None:
            cls._session = requests.Session()
            cls._ua = UserAgent()

            cls._session.headers.update({'User-Agent': cls._ua.random})
            cls._session.get("https://www.12306.cn/index/otn/login/conf")
        return cls._session


