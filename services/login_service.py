import time
import os
from requests import Response
from session_manager import SessionManager
import base64
import png


class LoginService:

    @classmethod
    def qr_login(clazz):

        # 下载二维码
        uuid, img_path = clazz.download_qr_code()
        
        # 循环检查二维码状态
        clazz.check_qr_code_status(uuid)

        # 移除二维码
        os.remove(img_path)

        # 登录
        return clazz.post_login()

    @classmethod
    def download_qr_code(clazz):    
        """下载二维码
        """
        response: Response = SessionManager.get_session().post(url='https://kyfw.12306.cn/passport/web/create-qr64', data = {'appid': 'otn'})
        try:
            body = response.json()
            img_bytes = base64.b64decode(body["image"])
            img_path = 'C:/Users/sloan.wang/Documents/12306/qr.png'
            # 确保目录存在
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            with open(img_path, 'wb') as file:
                    file.write(img_bytes)
            return body["uuid"], img_path
        except Exception as e:
            print('下载二维码失败:', str(e))
            return None, None

    @classmethod
    def check_qr_code_status(clazz, uuid) :
        """检查二维码状态
        """
        while uuid is not None:
            # 发送请求检查二维码状态
            response: Response = SessionManager.get_session().post(url='https://kyfw.12306.cn/passport/web/checkqr', data = {'uuid': uuid, 'appid': 'otn'})
            try:
                result_code = int(response.json()['result_code'])
                if result_code == 0:
                    print('等待扫描中...')
                elif result_code == 1:
                    print('已扫描，等待确认...')
                elif result_code == 2:
                    print('扫描成功')
                    break
                elif result_code == 3:
                    print('二维码已过期')
                    break
                time.sleep(1)
            except Exception as e:
                print('检查二维码状态失败:', str(e))
                break

    @classmethod
    def post_login(clazz):
        headers={
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'Origin': 'https://kyfw.12306.cn'
        }
        SessionManager.get_session().cookies.update(headers)
        SessionManager.get_session().get(url='https://kyfw.12306.cn/otn/login/userLogin', allow_redirects=True)
        new_tk = clazz.auth_uamtk()
        username =  clazz.auth_uamauthclient(new_tk)
        SessionManager.get_session().get(url='https://kyfw.12306.cn/otn/login/userLogin', allow_redirects=True)
        return username

    @classmethod
    def auth_uamtk(clazz):
        response = SessionManager.get_session().post("https://kyfw.12306.cn/passport/web/auth/uamtk", data={'appid': 'otn'})
        return response.json()['newapptk']

    @classmethod
    def auth_uamauthclient(clazz, tk):
        response = SessionManager.get_session().post("https://kyfw.12306.cn/otn/uamauthclient", data={'tk': tk})
        return response.json()['username']