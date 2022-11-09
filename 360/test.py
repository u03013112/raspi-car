import os
import cv2 
import Equirec2Perspec as E2P 

if __name__ == '__main__':
    equ = E2P.Equirectangular('image0 - image2b1.jpg')    # Load equirectangular image
    
    #
    # FOV unit is degree 
    # theta is z-axis angle(right direction is positive, left direction is negative)
    # phi is y-axis angle(up direction positive, down direction negative)
    # height and width is output image dimension 
    #
    img = equ.GetPerspective(90, 0, -0, 720, 1080) # Specify parameters(FOV, theta, phi, height, width)
    cv2.imwrite('1.jpg',img)

    img = equ.GetPerspective(90, 90, -0, 720, 1080) # Specify parameters(FOV, theta, phi, height, width)
    cv2.imwrite('2.jpg',img)

    img = equ.GetPerspective(90, 180, -0, 720, 1080) # Specify parameters(FOV, theta, phi, height, width)
    cv2.imwrite('3.jpg',img)

    img = equ.GetPerspective(90, -90, -0, 720, 1080) # Specify parameters(FOV, theta, phi, height, width)
    cv2.imwrite('4.jpg',img)