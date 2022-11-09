import  cv2

file_path = [
    'image0.jpg','image2.jpg'
]
img0 =cv2.imread(file_path[0])
img1 =cv2.imread(file_path[1])
img =cv2.hconcat([img0,img1])#水平拼接
# img=cv2.vconcat([img,img,img])#垂直拼接

cv2.imwrite('cat.jpg',img)