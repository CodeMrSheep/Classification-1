import torch
import torch.nn as nn
import timm
import inspect

import inspect
import timm.optim

optimizer_list = [
    "sgd",
    "adam",
    "lamb",
    "rmsproptf",
]


def create_optimizer(model, name, lr):
    """
    优化器入口

    model: 模型
    name: 优化器名称
    lr: 学习率
    """
    assert name in optimizer_list, "NotImplementedError"

    # optimizer = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=0.0005)
    if name in ["rmsproptf"]:
        optimizer = timm.optim.create_optimizer_v2(
            model, opt=name, lr=lr, weight_decay=0.0005, momentum=0.9, eps=0.001
        )
    else:
        optimizer = timm.optim.create_optimizer_v2(
            model, opt=name, lr=lr, weight_decay=0.0005, momentum=0.9
        )
    return optimizer
