import itertools

case_list = ['用户名', '密码']
value_list = ['正确', '不正确', '特殊符号', '超过最大长度']


def gen_case(item=case_list, value=value_list):
    '''输出笛卡尔用例集合'''
    for i in itertools.product(item, value):
        print('输入'.join(i))

def test_print():
     print("echo py kits")

if __name__ == '__main__':
    test_print()


# https://github.com/kennethreitz/setup.py
# https://mp.weixin.qq.com/s/-_FHb2Yq92vlHAuX4RS_UQ
# https://pypi.org/project/echo-py-kits/0.0.1/

# python3 -m pip install --user --upgrade setuptools wheel
# python setup.py sdist build

# pip install wheel twine
# python setup.py bdist_wheel --universal

# pip install twine
# twine check dist/*
# twine upload dist/*


# 本地安装测试
# pip install dist/mxxxxx-any.whl


# rm -rf ./dist && python setup.py sdist build && twine upload dist/*
# rm -rf ./dist && python setup.py sdist bdist_wheel && twine upload dist/*
