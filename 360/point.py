import cv2 

file_path = [
    'image0.jpg','image2.jpg'
]
img0 =cv2.imread(file_path[0])
img1 =cv2.imread(file_path[1])

points0 = [
    (1101,420),
    (1104,577),
    (1108,566),
    (1125,441),
    (1130,446),
]
for point in points0:
    img0 = cv2.circle(img0, point, 1, (0, 0, 255), 4)
cv2.imwrite('img0.jpg',img0)

points1 = [
    (173,467),
    (199,626),
    (196,614),
    (192,491),
    (197,498),
]
for point in points1:
    img1 = cv2.circle(img1, point, 1, (0, 0, 255), 4)
cv2.imwrite('img1.jpg',img1)


img2 = cv2.imread('cat.jpg')
points2 = [
    (1101,420),
    (1104,577),
    (1108,566),
    (1125,441),
    (1130,446),
    (173+1280,467),
    (199+1280,626),
    (196+1280,614),
    (192+1280,491),
    (197+1280,498),
]
for point in points2:
    img2 = cv2.circle(img2, point, 1, (0, 0, 255), 4)
cv2.imwrite('img2.jpg',img2)
