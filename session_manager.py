import requests
from requests import Session
from fake_useragent import UserAgent


class SessionManager:

    _session: Session | None = None
    _ua: UserAgent | None = None

    
    @classmethod
    def get_session(clazz) -> Session:

        if clazz._session is None:
            clazz._session = requests.Session()
            clazz._ua = UserAgent()

            clazz._session.headers.update({'User-Agent': clazz._ua.random})
            clazz._session.get("https://www.12306.cn/index/otn/login/conf")
        return clazz._session


