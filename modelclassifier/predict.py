# import the necessary packages
from tensorflow.keras.models import load_model

import numpy as np
import tensorflow as tf
import cv2
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


class Classifier:
    def __init__(self, lam, subset_size, extra, skips=7):
        self.model = load_model('./models/efficientb2(200)97%v3animal.h5')
        self.lb = pd.read_csv('./models/efficientb2(200)97%v3animalclasses')
        self.dictionary = {}
        self.final = {}
        self.skips = skips
        self.lam = lam
        self.extra = extra
        self.subset_size = subset_size

    def predict_vedio(self, filename):
        self.final = {}
        self.dictionary = {}
        import time
        from datetime import timedelta
        start = time.time()
        vs = cv2.VideoCapture(filename)
        count = 1
        while True:
            (grabbed, frame) = vs.read()
            if not grabbed:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (200, 200))
            preds = self.model.predict(np.array([frame]))
            psum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for p in preds:
                for i in range(10):
                    psum[i] = psum[i] + p[i]
            label = self.lb['class'].iloc[np.argmax(psum)]
            if label not in self.dictionary:
                self.dictionary[label] = [count]
            else:
                self.dictionary[label].append(count)
            count += self.skips
            vs.set(cv2.CAP_PROP_POS_FRAMES, count)
        vs.release()
        end = time.time()
        print("model time ", timedelta(seconds=end - start))

    def final_dict(self, res=None):
        l = []
        total = []
        for i in range(2, len(res)):
            if res[i - 1] - res[i - 2] <= self.lam:
                l.append(res[i - 2])
            elif res[i - 1] - res[i - 2] > self.lam:
                total.append(l)
                l = []
        if len(l) == len(res) - 2:
            total.append(l)
        return total

    def check(self):
        d = {}
        l = []
        for i, j in self.final.items():
            for k in j:
                if len(k) > self.subset_size:
                    if k[0] <= 7:
                        k[0] = 1
                        if self.extra - k[-1] <= 7:
                            k[-1] = self.extra
                        else:
                            k[-1] = k[-1] + 7
                    else:
                        k[0] = k[0] - 7
                    l.append([k[0],k[-1]])
            if len(l) != 0:
                d[i] = l
            l = []

        return d

    def longest_sequence(self):
        for i, j in self.dictionary.items():
            self.final[i] = Classifier.final_dict(self, j)
        return Classifier.check(self)
