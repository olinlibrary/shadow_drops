
import numpy as np
import cv2
import pymunk


class Contour(object):

    def __init__(self, mass):
        self.something = 0
        self.body = pymunk.Body(mass)

    def video_contour(self):
        cap = cv2.VideoCapture(0)

        while(True):
        	# Capture frame-by-frame
            ret, frame = cap.read()

            # transform image to grayscale and blur
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            blur = cv2.GaussianBlur(gray,(5,5),0)

            # color thresholds for binary image
            lower_color = np.array([0,0,0], dtype = "uint8")
            upper_color = np.array([115,115,115], dtype = "uint8")

            # create binary image
            binary_img = cv2.inRange(blur, lower_color, upper_color)

            # dilate image
            kernel = np.ones((5,5), np.uint8)
            img_erode = cv2.erode(binary_img, kernel, iterations=1)
            img_dilation = cv2.dilate(img_erode, kernel, iterations=1)
            opening = cv2.morphologyEx(img_dilation, cv2.MORPH_OPEN, kernel)

            # find thresholds for contouring
            ret,thresh = cv2.threshold(opening,0,115,cv2.THRESH_BINARY)

            # contour
            contours, hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            tuple_contours = self.convert_contour(contours)
            self.update_contour_object(tuple_contours)
            # draw contour on the dilated image
            #for c in contours:
                #cv2.drawContours(frame, [c], -1, (255,0,0), 3)

             # Display the resulting frame
            #cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def update_contour_object(self, contour_list):
        self.contour = pymunk.Poly(self.body, contour_list)
        #print(self.contour)

    def convert_contour(self, contour_list):
        contour_lst_of_tuples = []
        for i in contour_list:
            for j in i:
                for k in j:
                    contour_lst_of_tuples.append(tuple(k))
        return(contour_lst_of_tuples)

if __name__ == '__main__':
    testContour = Contour(1)
    testContour.video_contour()
