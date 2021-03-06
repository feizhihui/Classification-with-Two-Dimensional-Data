# encoding=utf-8


import tensorflow as tf
from dataloader3 import DataLoader
from cnn_model import CNNModel
import sklearn.metrics  as metrics
import os

# LD_LIBRARY_PATH   	/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def eval_print(y_true, y_pred, y_scores):
    print("accuracy %.6f" % metrics.accuracy_score(y_true, y_pred))
    print("Precision %.6f" % metrics.precision_score(y_true, y_pred))
    print("Recall %.6f" % metrics.recall_score(y_true, y_pred))
    print("f1_score %.6f" % metrics.f1_score(y_true, y_pred))
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_scores)
    print("auc_socre %.6f" % metrics.auc(fpr, tpr))


epoch_num = 5

batch_size = 256

keep_pro = 0.75

loader = DataLoader()
model = CNNModel()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

with tf.Session(config=config) as sess:
    sess.run(tf.global_variables_initializer())
    print('begin training:')
    for epoch in range(epoch_num):
        loader.shuffle()
        for iter, indices in enumerate(range(0, loader.train_size, batch_size)):
            batch_X = loader.train_X[indices:indices + batch_size]
            batch_Y = loader.train_Y[indices:indices + batch_size]
            y_pred, y_scores, loss, _ = sess.run(
                [model.y_pred, model.y_score, model.loss, model.train_op],
                feed_dict={model.X: batch_X, model.Y: batch_Y, model.keep_prob: keep_pro})
            if iter % 10 == 0:
                print("===Training Epoch{:d}/{:d} Iter:{:d}/{:d}===".format(epoch + 1, epoch_num, iter + 1,
                                                                            loader.train_size // batch_size))
                print('loss: %.3f' % loss)
                eval_print(batch_Y, y_pred, y_scores)

    # store
    saver = tf.train.Saver()
    saver.save(sess, '../model/cnn_model')
