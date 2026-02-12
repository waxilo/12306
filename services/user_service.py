from requests import Response
from session_manager import SessionManager

class UserService:

    @classmethod
    def user_info(clazz):
        SessionManager.get_session().headers.update({
            'Referer': 'https://kyfw.12306.cn/otn/view/information.html'
        })
        response: Response = SessionManager.get_session().post('https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi')
        try:
            return response.json()
        except Exception as e:
            print('获取用户信息失败，响应:', response.text, str(e))
            return None