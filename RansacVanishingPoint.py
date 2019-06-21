import numpy as np
import random
import matplotlib.pyplot as plt
import cv2

origin = cv2.imread('fog_new.png')
class Model(object):
    def fit(self, data):
        raise NotImplementedError

    def distance(self, data):
        raise NotImplementedError


class Line(object):
    def __init__(self, line):
        self.x1 = line[0]
        self.y1 = line[1]
        self.x2 = line[2]
        self.y2 = line[3]


class pointModel(Model):
    def __init__(self):
        self.params = None
        self.residual = 0

    def fit(self, lines):
        lines = lines[:, 0]
        X = []
        Y = []
        for i in range(len(lines) - 1):
            line1 = Line(lines[i])
            line2 = Line(lines[i + 1])
            x, y = getcrosspoint(line1, line2)
            X.append(x)
            Y.append(y)
        X = np.asarray(x).mean()
        Y = np.asarray(y).mean()
        self.params = [X, Y]
        for i in range(len(lines)):
            line = Line(lines[i])
            a, b, c = getlineparam(line)
            self.residual += (a * X + b * Y + c) / np.sqrt(a * a + b * b)

    def distance(self, samplelines):
        dists = []
        for line in samplelines:
            line = Line(line[0, :])
            [x, y] = self.params
            a, b, c = getlineparam(line)
            dist = abs((a * x + b * y + c) / np.sqrt(a * a + b * b))
            dists.append(dist)
        return np.asarray(dists)


def getlineparam(line):
    """
    For the line equation a*x+b*y+c=0, if we know two points(x1, y1)(x2,y2) in line, we can get
        a = y1 - y2
        b = x2 - x1
        c = x1*y2 - x2*y1
    """
    a = line.y1 - line.y2
    b = line.x2 - line.x1
    c = line.x1 * line.y2 - line.x2 * line.y1
    return a, b, c
def getcrosspoint(line1, line2):
    """
    if we have two lines: a1*x + b1*y + c1 = 0 and a2*x + b2*y + c2 = 0,
    when d(= a1 * b2 - a2 * b1) is zero, then the two lines are coincident or parallel.
    The cross point is :
        x = (b1 * c2 - b2 * c1) / d
        y = (a2 * c1 - a1 * c2) / d
    """
    a1, b1, c1 = getlineparam(line1)
    a2, b2, c2 = getlineparam(line2)
    d = a1 * b2 - a2 * b1
    if d == 0:
        return np.inf, np.inf
    x = (b1 * c2 - b2 * c1) / d
    y = (a2 * c1 - a1 * c2) / d
    return x, y


def ransac(lines, model, min_inliers, iterations=100, eps=1, random_seed=42):
    """
    Fits a model to observed data.

    Uses the RANSC iterative method of fitting a model to observed data.
    """
    random.seed(random_seed)

    if len(lines) <= 2:
        raise ValueError("Not enough input lines to fit the model.")

    if 0 < min_inliers and min_inliers < 1:
        min_inliers = int(min_inliers * len(lines))

    best_params = None
    best_inliers = None
    best_residual = np.inf
    best_iteration = None

    for i in range(iterations):
        indices = list(range(len(lines)))
        random.shuffle(indices)
        inliers = np.asarray([lines[i] for i in indices[:2]])
        shuffled_lines = np.asarray([lines[i] for i in indices[2:]])
        try:
            model.fit(inliers)
            dists = model.distance(shuffled_lines)
            more_inliers = shuffled_lines[np.where(dists <= eps)[0]]
            inliers = np.concatenate((inliers, more_inliers))

            if len(inliers) >= min_inliers:
                model.fit(inliers)
                if model.residual < best_residual:
                    best_params = model.params
                    best_inliers = inliers
                    best_residual = model.residual
                    best_iteration = i

        except ZeroDivisionError as e:
            print(e)

    if best_params is None:
        raise ValueError("RANSAC failed to find a sufficiently good fit for the data.")
    else:
        return (best_params, best_inliers, best_residual, best_iteration)


# process a lane line image directly
img = origin
# plt.figure(figsize=(15,5))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(gray,cmap='gray')
# plt.show()

# canny edge detection to get the edge graph
blur_ksize = 5  # Gaussian blur kernel size
blured = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0, 0)
low_threshold = 20 # Canny edge detection low threshold
high_threshold = 80  # Canny edge detection high threshold
canny = cv2.Canny(blured, low_threshold, high_threshold)

# cv2.imshow('Canny edge', canny)
# cv2.waitKey()
def roi_mask(img, vertices):
  mask = np.zeros_like(img)
  mask_color = 255
  cv2.fillPoly(mask, vertices, mask_color)
  masked_img = cv2.bitwise_and(img, mask)
  return masked_img

roi_vtx = np.array([[(0, 550), (600, 450), (800, 450), (1400, 550)]])
roi_edges = roi_mask(canny, roi_vtx)
# plt.figure(figsize=(15,5))
# plt.imshow(roi_edges, cmap='gray')
# plt.show()

# use Hough Transform for line detection
rho = 1
theta = np.pi / 180
threshold = 30
min_line_length = 150
max_line_gap = 20

def draw_lines(img, lines, color=[255, 255, 255], thickness=1):
  for line in lines:
    for x1, y1, x2, y2 in line:
      cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold,
                min_line_len, max_line_gap):
  lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                          minLineLength=min_line_len,
                          maxLineGap=max_line_gap)
  line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
  draw_lines(line_img, lines)
  return line_img, lines


line_img, lines= hough_lines(roi_edges, rho, theta, threshold,  min_line_length, max_line_gap)

# cv2.imshow('hough line', line_img)
# cv2.waitKey()
Model = pointModel()
(params, inliers, residual, iteration) = ransac(lines, Model, 0.5, eps=1)
# cv2.line(line_img, (int (params[0]),int (params[1])), (int (params[0]), int  (params[1])), (0, 0, 255), 10)
# cv2.imshow("Diem Chan Troi", line_img)
# cv2.waitKey()
def VanishingPoint():
    return params