import urllib


class SearchResult:
    
    def __init__(self, data_str: str):
       self.arr = data_str.split('|')

    def decryptField(self):
        """解密加密字段
        Returns:
            解密后的字段值
        """
        return urllib.parse.unquote(self.arr[0])

    def getTrainNo(self):
        """获取列车号
        Returns:
            列车号，如 'G1234'
        """
        return self.arr[3]

    def getStartStation(self):
        """获取始发站编码
        Returns:
            出发站编码，如 'BJP'
        """
        return self.arr[4]

    def getEndStation(self):
        """获取终点站编码
        Returns:
            到达站编码，如 'SHH'
        """
        return self.arr[5]

    def getFromStation(self):
        """获取出发站编码
        Returns:
            出发站编码，如 'BJP'
        """
        return self.arr[6]

    def getToStation(self):
        """获取到达站编码
        Returns:
            到达站编码，如 'SHH'
        """
        return self.arr[7]

    def getDepartureTime(self):
        """获取出发时间
        Returns:
            出发时间，格式如 '08:00'
        """
        return self.arr[8]
    
    def getArrivalTime(self):
        """获取到达时间
        Returns:
            到达时间，格式如 '14:30'
        """
        return self.arr[9]

    def getDuration(self):
        """获取行程时间
        Returns:
            行程时间，格式如 '02:30'
        """
        return self.arr[10]
