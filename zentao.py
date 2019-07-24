import requests
import requests.cookies
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class ZenTao:
    host = str
    cookies = requests.cookies.RequestsCookieJar()
    session_name = str
    session_id = str
    session = requests.Session

    def __init__(self, host: str):
        """
        初始化类
        :param host: 服务器地址
        """
        self.host = host
        self.session = requests.Session()

    def login(self, username: str, password: str):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 是否成功
        """
        respond = self.session.get(self.host + '/zentao/api-getsessionid.json')
        if respond.status_code != 200:
            return False
        data = respond.json()
        # print(data)
        if data['status'] != 'success':
            return False

        data = json.loads(data['data'])

        self.cookies = respond.cookies
        self.session_name = data['sessionName']
        self.session_id = data['sessionID']

        params = {
            'account': username,
            'password': password
        }
        # self.session.cookies =
        respond = self.session.get(
            self.host + '/zentao/user-login.json?{0}={1}'.format(self.session_name, self.session_id),
            params=params, cookies=self.cookies)
        # print(req.content)
        if respond.status_code != 200:
            return False
        data = respond.json()
        if data['status'] != 'success':
            return False
        return True

    def logout(self):
        """
        退出
        :return: 是否成功
        """
        respond = self.session.get(
            self.host + '/zentao/user-logout.json?{0}={1}'.format(self.session_name, self.session_id))
        if respond.status_code != 200:
            return False
        data = respond.json()
        # print(data)
        if data['status'] != 'success':
            return False
        return True

    def create_build(self, product: int, project: int, name: str, builder: str, source: str, download: str,
                     attaches: [str], describe: str, uid: str):
        params = {"projectID": project}
        # respond = self.session.post(
        #     self.host + '/zentao/build-create-{0}.json?{1}={2}'.format(str(project), self.session_name,
        #                                                                self.session_id),
        #     params=params, cookies=self.cookies)
        respond = requests.get(
            self.host + '/zentao/build-view-1.json', cookies=self.cookies)
        if respond.status_code != 200:
            return False
        print(respond.content)
        # data = respond.json()
        # print(data)
        # if data['status'] != 'success':
        #     return False

        # data = MultipartEncoder(fields={
        #     'product': product,
        #     'name': name,
        #     'builder': builder,
        #     'date': '2019-1-1',
        #     'scmPath': source,
        #     'filePath': download,
        #     'labels[]': 'hello.c',
        #
        #     'files[]': [
        #
        #     ],
        #     'desc': describe,
        # 'uid': uid
        # })
        text_data = '''
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="product"

1
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="name"

v2
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="builder"

admin
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="date"

2019-07-24
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="scmPath"

source
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="filePath"

download
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="labels[]"

dns.bat
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="files[]"; filename="dns.bat"
Content-Type: application/octet-stream

ipconfig /flushdns
pause
Content-Disposition: form-data; name="labels[]"


------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="files[]"


------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="desc"

desc
------WebKitFormBoundarycme3r6RqAizMDt6Y
Content-Disposition: form-data; name="uid"

5d384077831fd
------WebKitFormBoundarycme3r6RqAizMDt6Y--
        '''
        header = 'multipart/form-data; boundary=----WebKitFormBoundarycme3r6RqAizMDt6Y'
        # decode_data = data.to_string()

        respond = self.session.post(
            self.host + '/zentao/build-create-{0}.json?{1}={2}'.format(str(project), self.session_name,
                                                                       self.session_id),
            data=text_data, headers={
                'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundarycme3r6RqAizMDt6Y'})
        if respond.status_code != 200:
            return False
        print(respond.content)
        return True

    @staticmethod
    def multipart_header(self, uuid: str):
        return {'Content-Type': 'multipart/form-data; boundary={0}'.format(uuid), 'charset': 'UTF-8'}

    @staticmethod
    def multipart_data(self, uuid: str, content: str):
        return ''


if __name__ == '__main__':
    z = ZenTao('http://127.0.0.1:80')
    if z.login('admin', 'jiangwq='):
        print("登录成功")
    if z.create_build(1, 1, 'v3', 'admin', 'github', 'ftp', [], 'desc', '5d384077831fd'):
        print("创建成功")
    if z.logout():
        print("注销成功")
