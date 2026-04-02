import cv2
import numpy as np
import os

image_path = r"/Users/atchayaramesh/Downloads/images/frame_00113.bmp"

frame = cv2.imread(image_path)
if frame is None:
    print("❌ Image not loaded")
    exit()

h, w = frame.shape[:2]
x1 = int(w * 0.31)
x2 = int(w * 0.48)
crop = frame[:, x1:x2]

print("Total Height:", h, "px")
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow("Threshold", thresh)
#cv2.waitKey(0)
h, w = thresh.shape
gap_rows = []

for y in range(h):
    row = thresh[y]
    black_pixels = np.sum(row == 0)

    if black_pixels > (w * 0.95):
        gap_rows.append(y)

gaps = []

if len(gap_rows) > 0:
    start = gap_rows[0]

    for i in range(1, len(gap_rows)):
        if gap_rows[i] != gap_rows[i-1] + 1:
            end = gap_rows[i-1]
            gaps.append((start, end))
            start = gap_rows[i]

    gaps.append((start, gap_rows[-1]))

filtered_gaps = []

for (y1, y2) in gaps:
    gap_height = y2 - y1

    if gap_height > 40:   
        filtered_gaps.append((y1, y2))

total_gap_height = 0

output = crop.copy()

for (y1, y2) in filtered_gaps:

    gap_height = y2 - y1
    cv2.rectangle(output,(0, y1),(w, y2),(0,255,0), 3)
    cv2.putText(output,f"{gap_height}px",(10, y1 + 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0), 2)
save_dir ="output"
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "gap_output.bmp")
cv2.imwrite(save_path, output)
cv2.imshow("GAP OUTPUT", output)
cv2.waitKey(0)
cv2.destroyAllWindows()