from flask import Flask, request, jsonify
import os
import imghdr

app = Flask(__name__, static_folder='.')

# 配置允许上传的文件类型和最大文件大小
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_storage):
    # 检查文件大小
    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)
    
    if size > MAX_FILE_SIZE:
        return False, "文件大小超过5MB限制"
    
    # 读取文件内容并验证是否为图片
    image_bytes = file_storage.read()
    file_storage.seek(0)
    
    image_format = imghdr.what(None, h=image_bytes)
    if image_format not in ['jpeg', 'png']:
        return False, "上传的文件不是有效的图片格式"
    
    return True, "验证通过"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'screenshot' not in request.files:
        return jsonify({'success': False, 'message': '未找到截图文件'}), 400
    
    file = request.files['screenshot']
    name = request.form.get('name', '').strip()
    
    if not name:
        return jsonify({'success': False, 'message': '请输入姓名'}), 400
    
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '不支持的文件格式'}), 400
    
    # 验证图片
    is_valid, message = validate_image(file)
    
    if not is_valid:
        return jsonify({
            'success': False,
            'message': message
        }), 400
    
    # 保存验证记录
    # 这里简化处理，实际应用中应该保存到数据库
    submissions_dir = 'submissions'
    if not os.path.exists(submissions_dir):
        os.makedirs(submissions_dir)
    
    # 保存截图
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    safe_filename = f"{name}_{int(os.path.getmtime(submissions_dir) if os.path.exists(submissions_dir) else 0)}.{file_ext}"
    file.save(os.path.join(submissions_dir, safe_filename))
    
    return jsonify({
        'success': True,
        'message': f'验证成功！{name}的环境配置截图已提交。我们会尽快审核。'
    })

if __name__ == '__main__':
    app.run(port=8000)
