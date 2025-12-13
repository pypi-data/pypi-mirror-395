import requests
import os
import base64
import hashlib


class WeChatWorkSender:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """获取企业微信的 access_token"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        response = requests.get(url)
        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise Exception(f"Failed to get access token: {result}")

    def upload_media(self, media_type, media_path):
        """上传文件或图片，获取 media_id"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={media_type}"
        files = {'media': open(media_path, 'rb')}
        response = requests.post(url, files=files)
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"Failed to upload media: {result}")

    def send_text(self, user_ids, content):
        """发送文本消息（返回完整响应，包含msgid）"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {"content": content}
        }
        response = requests.post(url, json=data)
        return response.json()  # 包含msgid的完整响应

    def send_image(self, user_ids, image_path):
        """发送图片消息（返回完整响应，包含msgid）"""
        media_id = self.upload_media('image', image_path)
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {"media_id": media_id}
        }
        response = requests.post(url, json=data)
        return response.json()  # 包含msgid的完整响应

    def send_file(self, user_ids, file_path):
        """发送文件消息（返回完整响应，包含msgid）"""
        media_id = self.upload_media('file', file_path)
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "file",
            "agentid": self.agentid,
            "file": {"media_id": media_id}
        }
        response = requests.post(url, json=data)
        return response.json()  # 包含msgid的完整响应

    def upload_file(self, webhook_url, excel_file_path):
        """向群聊上传文件，获取 media_id"""
        webhook_key = webhook_url.split("key=")[1]
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=file"
        with open(excel_file_path, "rb") as file:
            files = {"media": file}
            response = requests.post(url, files=files)
        data = response.json()
        if data["errcode"] == 0:
            return data["media_id"]
        else:
            raise Exception(f"Failed to upload file to group: {data}")

    def send_text_to_group(self, webhook_url, text_message, mentioned_list=None):
        """发送群聊文本消息（返回完整响应，包含msgid）"""
        if mentioned_list is None:
            mentioned_list = ["@all"]
        text_message_dict = {
            "msgtype": "text",
            "text": {
                "content": text_message,
                "mentioned_list": mentioned_list
            }
        }
        response = requests.post(webhook_url, json=text_message_dict)
        return response.json()  # 包含msgid的完整响应

    def send_file_to_group(self, webhook_url, file_path):
        """发送群聊文件消息（返回完整响应，包含msgid）"""
        media_id = self.upload_file(webhook_url, file_path)
        file_message = {
            "msgtype": "file",
            "file": {"media_id": media_id}
        }
        response = requests.post(webhook_url, json=file_message)
        return response.json()  # 包含msgid的完整响应

    # 新增：发送群聊图片消息（基于base64和md5）
    def send_image_to_group(self, webhook_url, image_path):
        """
        发送图片到群聊（Webhook）
        :param webhook_url: 群聊Webhook地址
        :param image_path: 本地图片路径（支持JPG/PNG，不超过2M）
        :return: 接口响应结果（包含msgid）
        """
        # 1. 验证图片大小（不超过2M）
        max_size = 2 * 1024 * 1024  # 2MB
        if os.path.getsize(image_path) > max_size:
            raise ValueError(f"图片大小超过2M限制，当前大小：{os.path.getsize(image_path) / 1024 / 1024:.2f}M")

        # 2. 读取图片并计算base64和md5
        with open(image_path, 'rb') as f:
            image_data = f.read()
            # 计算base64编码
            base64_str = base64.b64encode(image_data).decode('utf-8')
            # 计算md5（编码前的原始数据）
            md5_str = hashlib.md5(image_data).hexdigest()

        # 3. 构造图片消息体
        image_message = {
            "msgtype": "image",
            "image": {
                "base64": base64_str,
                "md5": md5_str
            }
        }

        # 4. 发送消息到群聊Webhook
        response = requests.post(webhook_url, json=image_message)
        return response.json()

    def recall_message(self, msgid):
        """
        撤回企业微信应用消息
        :param msgid: 要撤回的消息ID，从发送消息接口获取
        :return: 接口返回结果
        """
        if not msgid:
            raise ValueError("消息ID(msgid)不能为空")

        # 确保access_token有效（如果需要可以添加过期检查和刷新逻辑）
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/recall?access_token={self.access_token}"

        # 构建请求体
        data = {
            "msgid": msgid
        }

        try:
            response = requests.post(url, json=data)
            result = response.json()

            # 检查接口调用结果
            if result.get('errcode') == 0:
                print(f"消息撤回成功，msgid: {msgid}")
            else:
                print(f"消息撤回失败，错误码: {result.get('errcode')}, 错误信息: {result.get('errmsg')}")

            return result
        except Exception as e:
            raise Exception(f"撤回消息时发生错误: {str(e)}")

    # ========== 新增：发送Markdown消息（应用凭证） ==========
    def send_markdown(self, user_ids, content):
        """
        给企业微信成员发送Markdown消息（返回完整响应，包含msgid）
        :param user_ids: 用户ID列表，如 ["zhangsan", "lisi"]
        :param content: Markdown格式的消息内容（支持企业微信官方MD语法）
        :return: 接口响应结果（包含msgid）
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "markdown",
            "agentid": self.agentid,
            "markdown": {"content": content}
        }
        response = requests.post(url, json=data)
        return response.json()  # 包含msgid的完整响应

    # ========== 新增：发送群聊Markdown消息（Webhook） ==========
    def send_markdown_to_group(self, webhook_url, content):
        """
        给企业微信群聊发送Markdown消息（Webhook，返回完整响应，包含msgid）
        :param webhook_url: 群聊Webhook地址
        :param content: Markdown格式的消息内容（支持企业微信官方MD语法）
        :return: 接口响应结果（包含msgid）
        """
        markdown_message = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        response = requests.post(webhook_url, json=markdown_message)
        return response.json()  # 包含msgid的完整响应