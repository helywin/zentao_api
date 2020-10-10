# encoding:utf-8
import requests
import warnings
import json
import os
import time
import mimetypes
from requests_toolbelt import MultipartEncoder


class ZenTao:
    """
    控制禅道的类
    """
    host = str
    session_name = str
    session_id = str
    session = requests.Session
    boundary = str
    multipart_header = {}

    def __init__(self, host: str):
        self.host = host
        self.session = requests.Session()
        self.boundary = '------WebKitFormBoundaryAmOiBfmEYFBzUOnO'
        self.multipart_header = {'Content-Type': 'multipart/form-data; boundary={0}'.format(self.boundary),
                                 'charset': 'UTF-8'}

    def login(self, username: str, password: str):
        """
        登录禅道
        :return: 是否成功
        """
        respond = self.session.get(self.host + '/zentao/api-getsessionid.json')
        # print(req_get_session.content)
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        content = respond.json()
        # print(content)
        if content['status'] != 'success':
            warnings.warn('获取链接session失败')
            return False
        # md5_value = hashlib.md5(content['data'])
        # if md5_value != content['md5']:
        #     warnings.warn("数据md5校验错误")
        #     return False
        data = json.loads(content['data'])
        self.session_name = data['sessionName']
        self.session_id = data['sessionID']
        # print(self.session_name + '=' + self.session_id)
        params = {'account': username, 'password': password}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        respond = self.session.post(self.host + '/zentao/user-login.json?{0}={1}'
                                    .format(self.session_name, self.session_id),
                                    params=params)
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        # print(respond.content)
        content = respond.json()
        if content['status'] != 'success':
            warnings.warn('登录失败')
            return False
        return True

    def logout(self):
        '''
        退出禅道
        :return: 是否成功
        '''
        respond = self.session.get(self.host + '/zentao/user-logout.json')
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        # print(respond.content)
        content = respond.json()
        if content['status'] != 'success':
            warnings.warn('登录失败')
            return False
        return True

    def get_index(self):
        """
        获取首页
        :return:
        """
        respond = self.session.get(self.host + '/zentao/branch-sort.json?{0}={1}'
                                   .format(self.session_name, self.session_id))
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        print(respond.content)
        return True

    def get_build(self, id: int):
        """
        获取版本
        :return:
        """
        data = {'buildID': id}
        req = self.session.get(
            self.host + '/zentao/build-view-{0}.json?{1}={2}'.format(
                str(id), self.session_name, self.session_id),
            params=data)
        if req.status_code != 200:
            warnings.warn('http error: %d' % req.status_code)
            return False
        # content = req.json()
        # print(req.headers)
        # data = json.loads(content['data'], 'utf-8')
        # print(data['title'])
        return True

    def create_build(self, product: int, project: int, name: str, builder: str, source: str, download: str,
                     files: list, desc: str):
        """
        获取版本
        :return:
        """
        data = {'projectID': project}
        respond = self.session.get(
            self.host + '/zentao/build-create-{0}.json?{1}={2}'
            .format(str(project), self.session_name, self.session_id),
            params=data)
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        print(respond.content)
        fields = {
            'product': str(product),
            'name': name,
            'builder': builder,
            'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
            'scmPath': source,
            'filePath': download,
            'desc': desc
        }
        file_index = 0
        for file_name in files:
            file_bin: bytes
            mime_type: str
            try:
                fd = open(file_name, 'rb')
                # mime_type = mimetypes.guess_type(file)[0]
                # if mime_type is None:
                mime_type = 'application/octet-stream'
                print(mime_type)
                file_bin = fd.read()
                fd.close()
            except IOError as err:
                warnings.warn('failed to open file: ' + file_name + ' with' + err.__str__())
                continue
            fields["files[" + str(file_index) + "]"] = (
                os.path.basename(file_name), file_bin, mime_type)
            file_index += 1
        data = MultipartEncoder(
            fields=fields
        )

        # print(data)

        respond = self.session.post(
            self.host + '/zentao/build-create-{0}.json?{1}={2}'
            .format(str(project), self.session_name, self.session_id),
            headers={'Content-Type': data.content_type, 'charset': 'UTF-8'}, data=data)
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        content = respond.json()
        if content['result'] != 'success':
            warnings.warn('创建失败')
            return False
        print(respond.content)

        return True

    def delete_build(self, id: int):
        """
        删除版本
        :return:
        """
        data = {'buildID': id, 'confirm': 'yes'}
        respond = requests.get(
            self.host + '/zentao/build-delete-{0}-yes.json?{1}={2}'.format(
                str(id), self.session_name, self.session_id),
            params=data)
        if respond.status_code != 200:
            warnings.warn('http error: %d' % respond.status_code)
            return False
        # content = req.json()
        print(respond.content)
        # data = json.loads(content['data'], 'utf-8')
        # print(data['title'])
        return True


# example code
if __name__ == '__main__':
    z = ZenTao('http://127.0.0.1:80')
    if z.login('admin', '123456'):
        print('登录成功')
    if z.create_build(1, 1, 'test', 'admin', 'github.com', 'ftp://192.168.1.1',
                      ['../a.zip', '../b.zip'], 'describe'):
        print("创建版本")
    if z.logout():
        print('注销成功')
