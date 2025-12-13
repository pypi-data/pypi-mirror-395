class VirtualMailbox:
    """
    虚拟邮箱类
    """
    config = {
        "password": None,
        "cookie": None,
        "authorization": None
    }
    # 创建邮箱
    def create_mailbox(self) -> dict:
        """
        创建邮箱
        """
        new_config = {
            "config": self.config.copy(),
            "email": ""
        }
        return new_config
    
    # 查询邮件
    def get_email(self) -> dict:
        """
        emails是一个字典列表,每一个字典中的格式是
            1. email_text: 邮件内容
            2. subject: 邮件主题
            3. from_address: 发送邮件的来源账号
        """
       
        new_config = {
            "config": self.config.copy(),
            "emails": []
        }
        return new_config