# 最佳实践

## 一. 准备数据

1. 假设数据集根路径为`/home/xxx/CatDog`  ，格式如下

```bash
├── cat
    ├── aaa.jpg
    ├── bbb.jpg
    ├── ....
├── dog
    ├── ccc.jpg
    ├── bbb.jpg
    ├── ....
```

2. 划分数据集，默认`Config/`下生成train.txt、test.txt。

```bash
python  ./ExtraTools/split_imgs.py  --ImgsPath=/home/xxx/CatDog  --Ratio=[0.8,0.2]  --Verify
```

- --ImgsPath    数据集根路径
- --Ratio           各类别均按指定比例分配train:test，默认[0.8, 0.2]
- --Verify          验证图像完整性(耗时，可删除该参数)



## 二. 训练

1. 配置`Config/train.yaml`

   ```yaml
   # ========================================数据集===================================
   DataSet:
     prefix: /home/xxx/CatDog     # 数据集根路径 
     category: {"cat":0,"dog":1}  # 类别
     ratio: 0.9 									 # train:val比例  
     sampler: "balance" 					 # 类别采样  normal:常规采样   balance:类别平衡采样
     batch: 8   									 # batch size
   # ========================================模型===================================
   Models: 
     backbone: resnet18   					# 主干网络  
     head: cross_entropy  					# 损失函数  
     optimizer: SGD       					# 优化器
   
   # ========================================训练===================================
   Train:
     lr: 0.001  										# 初始学习率
     epochs: 50 										# 总轮次
     milestones: [35,45] 					# 学习率衰减
   ```

2. 开始训练

   ```bash
   python train.py  --yaml ./Config/train.yaml  --txt ./Config/train.txt
   ```

   控制台输出

   ```bash
   ****************************
   TensorBoard | Checkpoint save to  /xxx/Classification/ExpLog/2022-02-24_15:20:41/ 
   
   ****************************
   The nums of trainSet: 144
   The nums of each class:  Counter({'cat': 73, 'dog': 71}) 
   
   ****************************
   The nums of valSet: 16
   The nums of each class:  Counter({'dog': 11, 'cat': 5}) 
   
   start epoch 0/50...
   ```

3. TensorBoard可视化

<div align=center><img src="./imgs/tsdb.gif" ></div>

## 三. 测试

1. 配置`Config/test.yaml`

   ```yaml
   # ========================================数据集===================================
   DataSet:
     prefix: /home/xxx/CatDog     # 数据集根路径 
     category: {"cat":0,"dog":1}  # 类别
     batch: 8   									 # batch size
    
   # ========================================模型===================================
   Models: 
     backbone: resnet18   					# 主干网络 
     checkpoint: /xxx/resnet18.pth # 权重路径  	
   ```

2. 测试

   ```bash
   python test.py   --yaml ./Config/test.yaml   --txt ./Config/test.txt
   ```

   控制台输出 

   ```bash
   checkpoint load /xxx/resnet18.pth
   ****************************
   The nums of testSet: 40
   The nums of each class:  Counter({'cat': 20, 'dog': 20}) 
   
   acc is 0.975
   Predict  0        1        
   Actual
   0        20       0        
   
   1        1        19       
   
   
   Predict    0          1          
   Actual
   0          1.0        0.0        
   
   1          0.05       0.95 
   ```
