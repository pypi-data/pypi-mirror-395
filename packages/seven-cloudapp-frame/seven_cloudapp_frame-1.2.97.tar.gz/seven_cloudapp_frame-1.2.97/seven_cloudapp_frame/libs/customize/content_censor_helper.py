# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-11-17 18:51:25
@LastEditTime: 2025-11-26 16:56:06
@LastEditors: HuangJianYi
@Description: 内容审查帮助类
"""
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData


class BOSCensorHelper:
    """
    :description: 百度云帮助类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_access_token(self):
        """
        :description:动态获取access_token
        :return: 
        :last_editors: HuangJianYi
        """
        api_key = share_config.get_value("censor_bos_config", {}).get("api_key", "")
        secret_key = share_config.get_value("censor_bos_config", {}).get("secret_key", "")
        request_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
        response = requests.get(request_url)
        if response:
            if "error" not in json.loads(response.text).keys():
                access_token = json.loads(response.text)["access_token"]
                redis_init = SevenHelper.redis_init(config_dict=config.get_value("platform_redis"))
                redis_init.set("baidu_access_token", access_token, ex=2591000)
                return access_token
            else:
                self.logger_error.error("【获取百度云access_token失败】" + response.text)
        return ""

    @classmethod
    def text_censor(self, text, conclusion_types = [1]):
        """
        :description: 百度云文本审核（https://cloud.baidu.com/doc/ANTIPORN/s/Vk3h6xaga）
        :param text：内容
        :param conclusion_types：允许审核通过的结果类型（1.合规，2.不合规，3.疑似，4.审核失败）
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        redis_init = SevenHelper.redis_init(config_dict=config.get_value("platform_redis"))
        access_token = redis_init.get("baidu_access_token")
        if not access_token:
            access_token = self.get_access_token()
        if not access_token:
            invoke_result_data.success = False
            invoke_result_data.error_code = "fail_access_token"
            invoke_result_data.error_message = "无法进行文本审核"
            return invoke_result_data
        params = {"text": text}
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            if "error_code" not in json.loads(response.text).keys():
                conclusion_type = response.json()["conclusionType"]
                if conclusion_type not in  conclusion_types:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "fail"
                    invoke_result_data.error_message = "文本违规"
                    return invoke_result_data
                invoke_result_data.data = conclusion_type
                return invoke_result_data
            else:
                self.logger_error.error("【百度云文本审核失败】" + response.text)
        invoke_result_data.success = False
        invoke_result_data.error_code = "fail"
        invoke_result_data.error_message = "无法进行文本审核"
        return invoke_result_data


class COSCensorHelper:
    """
    :description: 腾讯云帮助类,需要安装模块cos-python-sdk-v5 (>=1.9.23版本)
    :param {type} 
    :return: 
    :last_editors: HuangJianYi
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_cos_config(self):
        cos_config = share_config.get_value("censor_cos_config", None)
        if not cos_config:
            cos_config = share_config.get_value("cos_config", {})
        self.access_key = cos_config.get("access_key", "") # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.secret_key = cos_config.get("secret_key", "") # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.bucket_name = cos_config.get("bucket_name", "") # 桶名称
        if not self.bucket_name:
            self.bucket_name = cos_config.get("bucket", "")
        self.region = cos_config.get("end_point", "") # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
        self.token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
        self.scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填


    @classmethod
    def text_censor(self, text, key=None, labels=["Normal"]):
        """
        :description: 文本审核
        :param text(string): 当传入的内容为纯文本信息，原文长度不能超过10000个 utf8 编码字符。若超出长度限制，接口将会报错。
        :param Key(string): COS路径.
        :param labels: 该字段用于返回检测结果中所对应的优先级最高的恶意标签，表示模型推荐的审核结果，建议您按照业务所需，对不同违规类型与建议值进行处理。 返回值：Normal：正常，Porn：色情，Ads：广告，以及其他不安全或不适宜的类型。
        """
        from qcloud_cos import CosConfig
        from qcloud_cos import CosS3Client

        self.get_cos_config()
        invoke_result_data = InvokeResultData()
        try:
            client = CosS3Client(CosConfig(Region=self.region, SecretId=self.access_key, SecretKey=self.secret_key, Token=self.token, Scheme=self.scheme))
            response = client.ci_auditing_text_submit(
                Bucket = self.bucket_name,  # 桶名称
                Key=key,
                Content = text.encode("utf-8"),  # 需要审核的文本内容        
            )
            response_data = SevenHelper.json_loads(response)
            if "JobsDetail" not in response_data or "Label" not in response_data["JobsDetail"]:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "检测失败"
                return invoke_result_data
            if  response_data["JobsDetail"]["Label"] not in labels:
                invoke_result_data.success = False
                invoke_result_data.error_code = "fail"
                invoke_result_data.error_message = "文本违规"
                return invoke_result_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【腾讯云文本审核失败】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data

    @classmethod
    def image_censor(self, img_list, labels=None, result=None, score=None, biz_type=None, is_async=None, callback=None, freeze=None):
        """
        :description: 图片审核
        :param img_list(dict array): 需要审核的图片信息,每个array元素为dict类型，支持的参数如下:
                            Object: 存储在 COS 存储桶中的图片文件名称，例如在目录 test 中的文件 image.jpg，则文件名称为 test/image.jpg。
                                传入多个时仅一个生效，按 Content，Object， Url 顺序。
                            Url: 图片文件的链接地址，例如 http://a-1250000.cos.ap-shanghai.tencentcos.cn/image.jpg。
                                传入多个时仅一个生效，按 Content，Object， Url 顺序。
                            Content: 图片文件的内容，需要先经过 base64 编码。Content，Object 和 Url 只能选择其中一种，传入多个时仅一个生效，按 Content，Object， Url 顺序。
                            Interval: 截帧频率，GIF 图检测专用，默认值为5，表示从第一帧（包含）开始每隔5帧截取一帧
                            MaxFrames: 最大截帧数量，GIF 图检测专用，默认值为5，表示只截取 GIF 的5帧图片进行审核，必须大于0
                            DataId: 图片标识，该字段在结果中返回原始内容，长度限制为512字节
                            LargeImageDetect: 对于超过大小限制的图片是否进行压缩后再审核，取值为： 0（不压缩），1（压缩）。默认为0。
                                注：压缩最大支持32M的图片，且会收取压缩费用。
                            UserInfo: 用户业务字段。
                            Encryption(dict): 文件加密信息。如果图片未做加密则不需要使用该字段，如果设置了该字段，则会按设置的信息解密后再做审核。
                                            Algorithm(string): 当前支持`aes-256-ctr、aes-256-cfb、aes-256-ofb、aes-192-ctr、aes-192-cfb、aes-192-ofb、aes-128-ctr、aes-128-cfb、aes-128-ofb`，不区分大小写。以`aes-256-ctr`为例，`aes`代表加密算法，`256`代表密钥长度，`ctr`代表加密模式。
                                            Key(string): 文件加密使用的密钥的值，需进行 Base64 编码。当KeyType值为1时，需要将Key进行指定的加密后再做Base64 编码。Key的长度与使用的算法有关，详见`Algorithm`介绍，如：使用`aes-256-ctr`算法时，需要使用256位密钥，即32个字节。
                                            IV(string): 初始化向量，需进行 Base64 编码。AES算法要求IV长度为128位，即16字节。
                                            KeyId(string): 当KeyType值为1时，该字段表示RSA加密密钥的版本号，当前支持`1.0`。默认值为`1.0`。
                                            KeyType(int): 指定加密算法的密钥（参数Key）的传输模式，有效值：0（明文传输）、1（RSA密文传输，使用OAEP填充模式），默认值为0。
        :param labels(string array): 该字段用于返回检测结果中所对应的优先级最高的恶意标签，表示模型推荐的审核结果，建议您按照业务所需，对不同违规类型与建议值进行处理。 返回值：Normal：正常，Porn：色情，Ads：广告，以及其他不安全或不适宜的类型。
        :param result(int array): 该字段表示本次判定的审核结果，您可以根据该结果，进行后续的操作；建议您按照业务所需，对不同的审核结果进行相应处理。有效值：0（审核正常），1 （判定为违规敏感文件），2（疑似敏感，建议人工复核）。
        :param score: 该字段表示审核结果命中审核信息的置信度，取值范围：0（置信度最低）-100（置信度最高 ），越高代表该内容越有可能属于当前返回审核信息。例如：色情 99，表明该内容非常有可能属于色情内容
        :param biz_type(string): 审核策略的唯一标识，由后台自动生成，在控制台中对应为Biztype值.
        :param is_async(string): 是否异步进行审核，0：同步返回结果，1：异步进行审核。默认值为 0。
        :param callback(string): 审核结果（Detail版本）以回调形式发送至您的回调地址，异步审核时生效，支持以 http:// 或者 https:// 开头的地址，例如：http://www.callback.com。
        :param Freeze(dict): 可通过该字段，设置根据审核结果给出的不同分值，对图片进行自动冻结，仅当 input 中审核的图片为 object 时有效。
                    PornScore: 取值为[0,100]，表示当色情审核结果大于或等于该分数时，自动进行冻结操作。不填写则表示不自动冻结，默认值为空。
                    AdsScore: 取值为[0,100]，表示当广告审核结果大于或等于该分数时，自动进行冻结操作。不填写则表示不自动冻结，默认值为空。
        """
        from qcloud_cos import CosConfig
        from qcloud_cos import CosS3Client

        self.get_cos_config()
        invoke_result_data = InvokeResultData()
        try:
            client = CosS3Client(CosConfig(Region=self.region, SecretId=self.access_key, SecretKey=self.secret_key, Token=self.token, Scheme=self.scheme))
            response = client.ci_auditing_image_batch(Bucket=self.bucket_name, Input=img_list, BizType=biz_type, Async=is_async, Callback=callback, Freeze=freeze)
            response_data = SevenHelper.json_loads(response)
            if "JobsDetail" not in response_data:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "检测失败"
                return invoke_result_data
            fail_list = []
            for item in response_data["JobsDetail"]:
                if item.__contains__("Code") or (labels and item["Label"] not in labels) or (result and item["Result"] not in result) or (score and item["Score"] > score):
                    fail_list.append(item)
            if len(fail_list) > 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = "fail"
                invoke_result_data.error_message = "图片违规"
                invoke_result_data.data = fail_list
                return invoke_result_data
            return invoke_result_data
        except Exception as ex:
            self.logger_error.error("【腾讯云图片审核失败】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = traceback.format_exc()
            return invoke_result_data
