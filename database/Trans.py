from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models 
#有200w字符免费使用
SecretId = "你的ID"
SecretKey = "你的密钥"

class Translator:
    def __init__(self, from_lang, to_lang):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, text):
        try: 
            cred = credential.Credential(SecretId, SecretKey)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile) 

            req = models.TextTranslateRequest()
            req.SourceText = text
            req.Source = self.from_lang
            req.Target = self.to_lang
            req.ProjectId = 0

            resp = client.TextTranslate(req) 
            return resp.TargetText

        except TencentCloudSDKException as err: 
            return err

def trans_to_chinese(text):
    return Translator(from_lang='en', to_lang='zh').translate(text)

def trans_to_english(text):
    return Translator(from_lang='zh', to_lang='en').translate(text)

if __name__ == '__main__':
    print(trans_to_chinese('Hello')) 
    print(trans_to_english('Hello'))    