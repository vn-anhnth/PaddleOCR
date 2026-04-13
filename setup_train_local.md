# CLI train
- At D:\IEEE\data\phD:
  - .\env\Scripts\activate
- cd D:\IEEE\data\phD\PaddleOCR
  - python -m paddle.distributed.launch --gpus '0' tools/train.py -c configs/rec/license_plates/rec_svtrnet.yml -o Global.pretrained_model=D:/IEEE/data/phD/PaddleOCR/pretrained_models/rec_svtr_tiny_none_ctc_en_train/best_accuracy.pdparams

  - python -m paddle.distributed.launch --gpus '0' tools/eval.py -c configs/rec/license_plates/rec_svtrnet.yml -o Global.pretrained_model=D:/IEEE/data/phD/PaddleOCR/output/rec/svtr_1/best_model/model.pdparams

  - python tools/infer_rec.py -c "D:/IEEE/data/phD/PaddleOCR/configs/rec/license_plates/rec_svtrnet.yml" -o Global.infer_img="D:/IEEE/data/phD/data/50k_OCR/aaa_train_ne_version_5/test_dataset_for_perfomance/1k" Global.pretrained_model="D:/IEEE/data/phD/PaddleOCR/output/rec/svtr_1/best_model/model.pdparams" Global.save_res_path="D:/IEEE/data/phD/PaddleOCR/output/rec/svtr/rec_predict.txt"