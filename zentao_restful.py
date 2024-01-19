#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import time
import httpx

# get env ZENTAO_HOST, if not exist, set localhost
ZENTAO_HOST = os.getenv('ZENTAO_HOST', 'localhost')
ZENTAO_USER = os.getenv('ZENTAO_USER', 'admin')
ZENTAO_PASSWORD = os.getenv('ZENTAO_PASSWORD', '123456')
API_URL = 'zentao/api.php/v1'
DEBUG = True
TOKEN = None
print(f'ZENTAO_HOST: {ZENTAO_HOST}')
# class ZenTao:


def print_response(response):
    if response.status_code == 200 or response.status_code == 201:
        print('code:', response.status_code, 'succeed:', response.json())
    else:
        print('code:', response.status_code, 'failed:',
              json.loads(response.text).get('error'))


def get_tokens():
    """
    get tokens
    api: /tokens
    request method: POST
    request body:
        名称 	    类型 	必填 	描述
        account	    string	否	登录名
        password	string	否	密码
    response: { token: str }
    """
    global TOKEN
    data = {'account': ZENTAO_USER, 'password': ZENTAO_PASSWORD}
    url = f'http://{ZENTAO_HOST}/{API_URL}/tokens'
    if DEBUG:
        print('url:', url, 'request body:', data)
    response = httpx.post(url, json=data)
    if response.status_code == 200 or response.status_code == 201:
        TOKEN = response.json().get('token')
    print_response(response)


def get_user_myself():
    """
    get user myself info
    api: /user
    request method: GET
    request header: { Token: str }
    response:
        名称 	        类型 	必填 	描述
        profile	        object	是	
          ∟ id	        int	    是	用户编号
          ∟ type	    string	是	类型(inside 内部用户 | outside 外部用户)
          ∟ dept	    int	    是	所属部门
          ∟ account	    string	是	用户名
          ∟ realname	string	是	真实姓名
          ∟ nickname	string	否	昵称
          ∟ avatar	    string	否	头像
          ∟ birthday	date	否	生日
          ∟ gender	    string	否	性别(f 女性 | m 男性)
          ∟ mobile	    string	否	手机号码
          ∟ phone	    string	否	电话号码
          ∟ weixin	    string	否	微信号码
          ∟ address	    string	否	住址
          ∟ join	    date	否	加入日期
          ∟ admin	    boolean	是	是否管理员
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/user'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def get_user(user_id: int):
    """
    get user info
    api: /users/{id}
    request method: GET
    request header: { Token: str }
    response:
        名称 	    类型 	必填 	描述
        id	        int	    是	用户编号
        type	    string	是	类型(inside 内部用户 | outside 外部用户)
        dept	    int	    是	所属部门
        account	    string	是	用户名
        role	    string	是	角色
        realname	string	是	真实姓名
        nickname	string	否	昵称
        avatar	    string	否	头像
        birthday	date	否	生日
        gender	    string	否	性别(f 女性 | m 男性)
        email	    string	否	邮箱
        mobile	    string	否	手机号
        phone	    string	否	电话号
        weixin	    string	否	微信号
        join	    date	否	加入日期
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/users/{user_id}'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def get_products():
    """
    get products
    api: /products
    request method: GET
    request header: { Token: str }
    response: { products: object }
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/products'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def get_project_builds(project_id: int):
    """
    get builds
    api: /projects/{id}/builds
    request method: GET
    request header: { Token: str }
    response:
        名称 	        类型 	必填 	描述
        total	        int	    是	版本总数
        builds	        array	是	版本列表
          ∟ id	        int	    是	版本ID
          ∟ project	    int	    是	所属项目
          ∟ product	    int	    是	所属产品
          ∟ branch	    int	    是	所属分支
          ∟ execution	int	    是	所属执行
          ∟ name	    string	是	版本名称
          ∟ scmPath	    string	否	源代码地址
          ∟ filePath	string	否	下载地址
          ∟ date	    date	是	打包日期
          ∟ builder	    user	是	构建者
          ∟ desc	    string	是	版本描述
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/projects/{project_id}/builds'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def get_execution_builds(execution_id: int):
    """
    get builds
    api: /executions/{id}/builds
    request method: GET
    request header: { Token: str }
    response:
        名称 	        类型 	必填 	描述
        total	        int	    是	版本总数
        builds	        array	是	版本列表
          ∟ id	        int	    是	版本ID
          ∟ project	    int	    是	所属项目
          ∟ product	    int	    是	所属产品
          ∟ branch	    int	    是	所属分支
          ∟ execution	int	    是	所属执行
          ∟ name	    string	是	版本名称
          ∟ scmPath	    string	否	源代码地址
          ∟ filePath	string	否	下载地址
          ∟ date	    date	是	打包日期
          ∟ builder	    user	是	构建者
          ∟ desc	    string	是	版本描述
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/executions/{execution_id}/builds'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def get_build(build_id: int):
    """
    get build
    api: /builds/{id}
    request method: GET
    request header: { Token: str }
    response:
        名称 	    类型 	必填 	描述
        id	        int	    是	版本ID
        project	    int	    是	所属项目
        product	    int	    是	所属产品
        branch	    int	    是	所属产品分支（主分支为0）
        execution	int	    是	所属执行
        name	    string	是	版本名称
        scmPath	    string	是	源代码地址
        filePath	string	是	下载地址
        desc	    string	是	版本描述
        builder	    user	是	构建者
        date	    date	是	打包日期
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    url = f'http://{ZENTAO_HOST}/{API_URL}/builds/{build_id}'
    if DEBUG:
        print('url:', url, 'request header:', headers)
    response = httpx.get(url, headers=headers)
    print_response(response)


def create_build(project_id: int):
    """
    create build
    api: /projects/{id}/builds
    request method: POST
    request header: { Token: str }
    request body:
        名称 	    类型 	必填 	描述
        execution	int	    是	所属执行
        product	    int	    是	所属产品
        branch	    int	    否	所属分支
        name	    string	是	版本名称
        builder	    string	是	构建者
        date	    date	否	打包日期
        scmPath	    string	否	源代码地址
        filePath	string	否	下载地址
        desc	    string	否	版本描述
    response:
        名称 	    类型 	必填 	描述
        id	        int	    是	版本ID
        project	    int	    是	所属项目
        product	    int	    是	所属产品
        branch	    int	    是	所属产品分支（主分支为0）
        execution	int	    是	所属执行
        name	    string	是	版本名称
        scmPath	    string	是	源代码地址
        filePath	string	是	下载地址
        desc	    string	是	版本描述
        builder	    user	是	构建者
        date	    date	是	打包日期
    """
    global TOKEN
    if TOKEN is None:
        get_tokens()
    if TOKEN is None:
        return

    headers = {'Token': TOKEN}
    data = {'name': 'build name', 'desc': 'build desc', 'begin': int(
        time.time()), 'end': int(time.time()), 'status': 1}
    url = f'http://{ZENTAO_HOST}/{API_URL}/projects/{project_id}/builds'
    if DEBUG:
        print('url:', url, 'request header:', headers, 'request body:', data)
    response = httpx.post(url, headers=headers, json=data)
    print_response(response)


if __name__ == '__main__':
    get_tokens()
    get_user_myself()
    get_user(4)
    get_products()
