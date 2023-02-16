import random
import cv2
import numpy as np
import os
import tensorflow as tf


class DataGen(tf.keras.utils.Sequence):

    def __init__(self, path,
                 batch_size,
                 shuffle=True):

        self.path = path
        self.list_of_filenames = os.listdir(path + '/in')
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.data_size = len(self.list_of_filenames)
        self.aug_batch_size = batch_size//2

    def on_epoch_end(self):
        if self.shuffle:
            random.shuffle(self.list_of_filenames)


    def __getitem__(self, index):
        try:
            batches = self.list_of_filenames[index * self.aug_batch_size : (index + 1) * self.aug_batch_size]
        except IndexError:
            batches = self.list_of_filenames[index * self.aug_batch_size :]
        x_batch, y_batch = self.__get_data(batches)
        return x_batch, y_batch


    def __get_data(self, batches):
        images = []
        masks = []

        for img_name in batches:
            img = cv2.imread(self.path + '/in/' + img_name, cv2.IMREAD_GRAYSCALE)
            mask = cv2.imread(self.path + '/out/' + img_name, cv2.IMREAD_GRAYSCALE)
            images += [img]
            masks += [mask]

        aug_images = [0] * self.aug_batch_size
        aug_masks = [0] * self.aug_batch_size
        for i in range(self.aug_batch_size):
            r = random.randint(1,2)
            if r == 1:
                aug_images[i], aug_masks[i] = self.__rotated(images[i], masks[i])
            else:
                aug_images[i], aug_masks[i] = self.__contrast(images[i]), masks[i]

        images = images + aug_images
        masks = masks + aug_masks
        images = np.array(images) / 255.
        masks = np.array(masks) / 255.
        return images, masks


    def __rotated(self, img, mask):
        (h, w) = img.shape
        center = (int(w / 2), int(h / 2))
        angle = random.randint(0, 360)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 0.8)

        rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
        rotated_mask = cv2.warpAffine(mask, rotation_matrix, (w, h))

        return rotated, rotated_mask


    def __contrast(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel
        lab = cv2.merge((l2,a,b))  # merge channels
        img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        return img2


    def __len__(self):
        return self.data_size // self.aug_batch_size


data_gen = DataGen('C:/Users/User/PycharmProjects/pythonProject/Test',
                   batch_size=10,
                   shuffle=True)

print(data_gen.__len__())
indexes = [i for i in range(data_gen.__len__())]

batches = data_gen.__getitem__(1)
cv2.imshow('1', batches[0][7])
cv2.waitKey(0)

