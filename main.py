from flask import Flask, jsonify, render_template, request,jsonify
from PIL import Image
from torchvision import models, transforms
import torch
import io
# 创建Flask应用程序对象  
app = Flask(__name__)  

# 加载ResNet模型
resnet = models.resnet101(weights = models.ResNet101_Weights.IMAGENET1K_V2)
resnet.eval()
# 加载结果标签
with open('./data/imagenet_classes_chinese.txt', 'r') as f:
   labels =  [i.strip() for i in f.readlines()]
# 构建转化流程
preprocess = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = [0.485, 0.456, 0.406],
            std = [0.229, 0.224, 0.225]
        )
    ]
)
# 首页
@app.route('/')  
def index():  
    return render_template('index.html') 

# 接受发送来的预测数据
@app.route('/api/predict', methods=['POST'])
def predict():
    # 获取文件数据
    binary_file = request.files['image'].read()
    # 将二进制数据转换为内存文件对象
    image_file = io.BytesIO(binary_file)
    # 使用PIL打开内存文件对象
    image = Image.open(image_file).convert('RGB')
    image_t = preprocess(image)
    batch_t = torch.unsqueeze(image_t, 0) # 在第0个位置添加一个维度
    output = resnet(batch_t)
    val, idx = torch.max(output, 1)
    result = {'result':labels[idx[0]], 'precent': int(val)*10}
    response = jsonify(result)
    response.headers.add('Content-Type', 'application/json; charset=utf-8')
    # 显示结果
    return response
  
# 运行应用程序  
if __name__ == '__main__':  
    app.run(debug=True, port=8000)