import requests
import re
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
            
            user_agent = clazz._ua.random
            # 解析 User-Agent 生成 sec-ch-ua 相关字段
            sec_ch_ua = '"Not(A:Brand";v="8"'
            sec_ch_ua_platform = '"Windows"'
            
            # 根据 User-Agent 类型设置相应的浏览器信息
            if 'Chrome' in user_agent:
                # 提取 Chrome 版本
                match = re.search(r'Chrome/(\d+)', user_agent)
                if match:
                    chrome_version = match.group(1)
                    sec_ch_ua += ', "Chromium";v="{}", "Google Chrome";v="{}"'.format(chrome_version, chrome_version)
            elif 'Firefox' in user_agent:
                # 提取 Firefox 版本
                match = re.search(r'Firefox/(\d+)', user_agent)
                if match:
                    firefox_version = match.group(1)
                    sec_ch_ua += ', "Firefox";v="{}"'.format(firefox_version)
            
            clazz._session.headers.update({
                'User-Agent': user_agent,
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Origin': 'https://www.12306.cn',
                'Referer': 'https://www.12306.cn/index/index.html',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': sec_ch_ua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': sec_ch_ua_platform,
            })
            clazz._session.get("https://www.12306.cn/index/otn/login/conf")
        return clazz._session

    @classmethod
    def clear_session(clazz):
        clazz._session = None
        clazz._ua = None