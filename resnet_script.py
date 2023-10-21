from torchvision import models
from torchvision import transforms
from PIL import Image 
import torch
# 创建一个101层的resnet（残差网络）实例
resnet = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)

# 构建一个transform，可以将任何尺寸的图片转化为要求格式的数据

preprocss = transforms.Compose(
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

# 加载图像
image = Image.open('./photo/dog.jpg')
image_t = preprocss(image)
batch_t = torch.unsqueeze(image_t, 0)

resnet.eval() # 开启测试模式
output = resnet(batch_t)
_, index = torch.max(output, 1)

with open('./data/imagenet_classes.txt', 'r') as f:
   labels =  [i.strip() for i in f.readlines()]

print(labels[index[0]])
