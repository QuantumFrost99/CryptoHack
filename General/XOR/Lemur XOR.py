import cv2

flag = cv2.imread("D:\\Cryptography\\Crypto Hack\\XOR\\flag.png")
lemur = cv2.imread("D:\\Cryptography\\Crypto Hack\\XOR\\lemur.png") # Download the images to Run

value = cv2.bitwise_xor(flag,lemur)
cv2.imshow('ez',value)
cv2.waitKey(0)
cv2.destroyAllWindows(0)