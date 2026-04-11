# CLI train
- At D:\IEEE\data\phD:
  - .\env\Scripts\activate
- cd D:\IEEE\data\phD\PaddleOCR
  - python -m paddle.distributed.launch --gpus '0' tools/train.py -c configs/rec/license_plates/rec_svtrnet.yml -o Global.pretrained_model=D:/IEEE/data/phD/PaddleOCR/pretrained_models/rec_svtr_tiny_none_ctc_en_train/best_accuracy.pdparams