class SearchParams:
    
    def __init__(self, train_date=None, from_station=None, to_station=None, purpose_codes='ADULT'):
        """初始化查询参数
        Args:
            train_date: 乘车日期，格式如 '2026-02-15'
            from_station: 出发站编码，如 'BJP'
            to_station: 到达站编码，如 'SHH'
            purpose_codes: 票种代码，默认 'ADULT'
        """
        self.params = {}
        if train_date:
            self.params['leftTicketDTO.train_date'] = train_date
        if from_station:
            self.params['leftTicketDTO.from_station'] = from_station
        if to_station:
            self.params['leftTicketDTO.to_station'] = to_station
        if purpose_codes:
            self.params['purpose_codes'] = purpose_codes
    
    def get_params(self):
        """获取所有参数的字典
        Returns:
            参数字典
        """
        return self.params
