# encoding=utf-8


import tensorflow as tf
from  dataloader1 import DataLoader
from cnn_model import CNNModel
import sklearn.metrics  as metrics
import numpy as np
import os

# LD_LIBRARY_PATH   	/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def eval_print(y_true, y_pred, y_logits):
    print("accuracy %.6f" % metrics.accuracy_score(y_true, y_pred))
    print("Precision %.6f" % metrics.precision_score(y_true, y_pred))
    print("Recall %.6f" % metrics.recall_score(y_true, y_pred))
    print("f1_score %.6f" % metrics.f1_score(y_true, y_pred))
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_logits)
    print("auc_socre %.6f" % metrics.auc(fpr, tpr))


batch_size = 512

loader = DataLoader(train_mode=False)
model = CNNModel()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

with tf.Session(config=config) as sess:
    sess.run(tf.global_variables_initializer())
    # store
    saver = tf.train.Saver()
    saver.restore(sess, '../model/cnn_model')

    print('begin testing:')

    y_preds = []
    y_scores = []
    for iter, indices in enumerate(range(0, loader.test_size, batch_size)):
        batch_X = loader.test_X[indices:indices + batch_size]
        y_pred, y_score = sess.run([model.y_pred, model.y_score],
                                   feed_dict={model.X: batch_X, model.keep_prob: 1.0})

        y_preds.append(y_pred)
        y_scores.append(y_score)
        print("===Testing Iter:{:d}/{:d}===".format(iter + 1, loader.test_size // batch_size))
    y_preds = np.concatenate(y_preds, axis=0)
    y_scores = np.concatenate(y_scores, axis=0)
    eval_print(loader.test_Y, y_preds, y_scores)
