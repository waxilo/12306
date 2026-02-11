import time
import os
from requests import Response
from session_manager import SessionManager
import base64
import png


class LoginService:

    def qr_login(self):
        """实现二维码登录逻辑
        """
        # 下载二维码
        uuid, img_path = self.download_qr_code()
        # 控制台打印二维码
        self.print_qrcode(img_path)
        # 循环检查二维码状态
        flag = self.check_qr_code_status(uuid)

        # 登录成功，移除文件
        os.remove(img_path)

        return flag

    def download_qr_code(self):
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

    def check_qr_code_status(self, uuid):
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
                    return True
                elif result_code == 3:
                    print('二维码已过期')
                    return False
                time.sleep(1)
            except Exception as e:
                print('检查二维码状态失败:', str(e))
                return False

    def print_qrcode(self, path):
        reader = png.Reader(path)
        width, height, rows, info = reader.read()
        lines = list(rows)

        planes = info['planes']  # 通道数
        threshold = (2 ** info['bitdepth']) / 2  # 色彩阈值

        # 识别二维码尺寸
        x_flag = -1   # x 边距标志
        y_flag = -1   # y 边距标志
        x_white = -1  # 定位图案白块 x 坐标
        y_white = -1  # 定位图案白块 y 坐标

        i = y_flag
        while i < height:
            if y_white > 0 and x_white > 0:
                break
            j = x_flag
            while j < width:
                total = 0
                for k in range(planes):
                    px = lines[i][j * planes + k]
                    total += px
                avg = total / planes
                black = avg < threshold
                if y_white > 0 and x_white > 0:
                    break
                if x_flag > 0 > x_white and not black:
                    x_white = j
                if x_flag == -1 and black:
                    x_flag = j
                if y_flag > 0 > y_white and not black:
                    y_white = i
                if y_flag == -1 and black:
                    y_flag = i
                if x_flag > 0 and y_flag > 0:
                    i += 1
                j += 1
            i += 1

        assert y_white - y_flag == x_white - x_flag
        scale = y_white - y_flag

        assert width - x_flag == height - y_flag
        module_count = int((width - x_flag * 2) / scale)

        whole_white = '█'
        whole_black = ' '
        down_black = '▀'
        up_black = '▄'

        dual_flag = False
        last_line = []
        output = '\n'
        for i in range(module_count + 2):
            output += up_black
        output += '\n'
        i = y_flag
        while i < height - y_flag:
            if dual_flag:
                output += whole_white
            t = 0
            j = x_flag
            while j < width - x_flag:
                total = 0
                for k in range(planes):
                    px = lines[i][j * planes + k]
                    total += px
                avg = total / planes
                black = avg < threshold
                if dual_flag:
                    last_black = last_line[t]
                    if black and last_black:
                        output += whole_black
                    elif black and not last_black:
                        output += down_black
                    elif not black and last_black:
                        output += up_black
                    elif not black and not last_black:
                        output += whole_white
                else:
                    last_line[t:t+1] = [black]
                t = t + 1
                j += scale
            if dual_flag:
                output += whole_white + '\n'
            dual_flag = not dual_flag
            i += scale
        output += whole_white
        for i in range(module_count):
            output += up_black if last_line[i] else whole_white
        output += whole_white + '\n'
        print(output, flush=True)
