import cv2
import os
import numpy as np


class Contours:

    WHITE = 255
    BLACK = 0

    def __init__(self, img):
        self.img = img
        self.treshold()
        self.contours, self.hirerchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        self.hirerchy = self.hirerchy[0]
        self.len_of_white = 0
        self.areas = []
        self.contours_list = []

        self.ROI = []

    def treshold(self):
        for i in range(480):
            for j in range(640):
                if img[i, j] > 100:
                    img[i, j] = 255
                else:
                    img[i, j] = 0


    def find_black_point(self, contour):

        for p in range(len(contour)):
            start = contour[p][0]
            x = start[1]
            y = start[0]

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.img[x + i, y + j] == 0:
                        return x + i, y + j
            print("не нашел")



    def flood_fill(self, img, x, y, newColor):
        mask = np.zeros([482, 642], np.uint8)
        cv2.floodFill(img, seedPoint=(y, x), newVal=newColor, mask=mask)


    def get_image(self):
        return self.img


    def remove_ROI(self):
        maximum = 0
        index = 0
        lenght = self.len_of_white

        for i in range(lenght):
            if self.areas[i] > maximum:
                maximum = self.areas[i]
                index = i
        re = self.contours_list[index]
        self.ROI.append(re)

        new_contours = []

        for k in range(lenght):
            point = self.contours_list[k][0][0]
            if point[0] == re[0][0][0] and point[1] == re[0][0][1]:
                self.len_of_white -= 1
                continue
            new_contours.append(self.contours_list[k])

        self.contours_list = new_contours
        self.areas.remove(maximum)


    def check(self):
        area0 = cv2.contourArea(self.ROI[0])
        area1 = cv2.contourArea(self.ROI[1])
        if area0 > area1:
            if area0 > area1 * 3:
                point = self.ROI[1][0][0]
                x = point[1]
                y = point[0]
                self.flood_fill(self.img, x, y, self.BLACK)
        else:
            if area1 > area0 * 3:
                point = self.ROI[0][0][0]
                x = point[1]
                y = point[0]
                self.flood_fill(self.img, x, y, self.BLACK)



    def delete_white(self):
        for i in range(len(self.hirerchy)):
            if self.hirerchy[i][3] == -1:
                self.len_of_white += 1
                area = cv2.contourArea(self.contours[i])
                self.areas.append(area)
                self.contours_list.append(self.contours[i])

        if self.len_of_white == 1:
            return
        if self.len_of_white == 2:
            if min(self.areas) * 3 > max(self.areas):
                return
            else:
                self.ROI.append(self.contours_list[0])
                self.ROI.append(self.contours_list[1])
                self.check()
                return

        self.remove_ROI()
        self.remove_ROI()

        for i in range(self.len_of_white):
            point = self.contours_list[i][0][0]
            x = point[1]
            y = point[0]
            self.flood_fill(self.img, x, y, self.BLACK)

        self.check()
        return


    def delete_internals(self):
        self.hirerchy, self.contours = self.contours, self.hirerchy = cv2.findContours(img, cv2.RETR_CCOMP,
                                                                                       cv2.CHAIN_APPROX_NONE)
        self.hirerchy = self.hirerchy[0]
        for i in range(len(self.hirerchy)):
            if self.hirerchy[i][3] != -1:
                x, y = self.find_black_point(self.contours[i])
                self.flood_fill(self.img, x, y, self.WHITE)
