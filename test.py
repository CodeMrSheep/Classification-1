import sys
import os
import torch
import time
import yaml
from DataSets import create_dataloader
from Models.Backbone import create_backbone
from Utils.tools import eval_confusion_matrix
import argparse

cur_path = os.path.abspath(os.path.dirname(__file__))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument("--yaml", help="测试配置", default=cur_path + "/Config/test.yaml")
    parser.add_argument("--txt", help="测试集路径", default=cur_path + "/Config/test.txt")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    file = open(args.yaml, "r")
    cfg = yaml.load(file, Loader=yaml.FullLoader)
    cfg["DataSet"]["txt"] = args.txt

    model = create_backbone(
        cfg["Models"]["backbone"],
        num_classes=len(cfg["DataSet"]["category"]),
        checkpoint=cfg["Models"]["checkpoint"],
    )
    model.to(device)
    model.eval()

    test_dataloader = create_dataloader(cfg["DataSet"], mode="test")

    # 测试,输出ACC及混淆矩阵
    acc = eval_confusion_matrix(model, test_dataloader, device)
    print("accuracy is %.3f \n" % acc.Overall_ACC)
    acc.print_matrix()
    acc.print_normalized_matrix()
