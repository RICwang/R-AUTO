from flask import Flask, request, render_template, send_from_directory
from markupsafe import escape
import os
import logging
import logging.config

app = Flask(__name__)
# 修改这里的导入路径
app.config.from_object('config.app_config')
logging.config.dictConfig(app.config['LOGGING_CONFIG'])

# 配置文件夹路径
TMP_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
if not os.path.exists(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)

def return_success(data=dict()):
    return {
        'code': 0,
        'msg': 'success',
        'data': data
    }

def return_error(msg):
    return {
        'code': 1,
        'msg': msg
    }

@app.route('/update-vc/<path:vcPath>')
def viewUpdateVc(vcPath):
    # 获取url参数vc-path
    vcPath = escape(vcPath)
    app.logger.debug('测试: %s', vcPath)
    # # 获取上传文件夹中的所有图片文件
    image = os.path.join('/tmp', vcPath)
    return render_template('update-vc.html', image=image, vcPath=vcPath)

@app.route('/api/update-vc/<path:vcPath>', methods=['POST'])
def apiUpdateVc(vcPath):
    # 获取request中的参数
    data = request.get_json()
    if data is None:
        return return_error('No data found')
    vcString = data.get('vcString')
    # 将vcPath的后缀名去掉
    vcPath = os.path.splitext(vcPath)[0]
    # 拼接vcPath
    vcPath = os.path.join(TMP_FOLDER, vcPath)
    # 打印日志
    app.logger.debug(f'update vc: {vcPath}')
    # 将vcString写入文件vcPath，不存在则创建
    with open(vcPath, 'w') as f:
        f.write(vcString)

    return return_success()

if __name__ == '__main__':
    app.run(port=5000)