import cv2

def get_range(image):
    min = [255, 255, 255]
    max = [0, 0, 0]
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, w, c = hsv.shape
    for i in range(h):
        for j in range(w):
            for v in range(c):
                a = hsv[i][j][v]
                if a < min[v]:
                    min[v] = a
                if a > max[v]:
                    max[v] = a
    return min,max


image = cv2.imread("input.png")

min,max = get_range(image)
print(min,max)