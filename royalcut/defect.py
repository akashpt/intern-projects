import cv2
import os
import numpy as np

image_path = r"/Users/atchayaramesh/Downloads/images/frame_00029.bmp"

save_dir = "cropped_output"
os.makedirs(save_dir, exist_ok=True)

# Load image
frame = cv2.imread(image_path)
if frame is None:
    print("❌ Image not loaded")
    exit()

h, w = frame.shape[:2]
print(f"Image Size: {w} x {h}")

def crop_royalcut_belt(frame):
    h, w = frame.shape[:2]
    x1 = int(w * 0.31)
    x2 = int(w * 0.48)
    return frame[0:h, x1:x2]

crop = crop_royalcut_belt(frame)
cv2.imshow("RoyalCut Belt", crop)
save_path = os.path.join(save_dir, "belt_crop.bmp")
cv2.imwrite(save_path, crop)
print("✅ Saved:", save_path)

gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)


# Adaptive threshold
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Morphology to remove letters
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,5))
letters_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
letters_mask = cv2.morphologyEx(letters_mask, cv2.MORPH_CLOSE, kernel_close)

mask_clean = cv2.bitwise_not(letters_mask)

border_margin = int(crop.shape[0] * 0.05)
mask_clean[:border_margin, :] = 0
mask_clean[-border_margin:, :] = 0

# Apply mask 
masked_img = cv2.bitwise_and(blur, blur, mask=mask_clean)

edges = cv2.Canny(masked_img, 50, 150)
edges_dilated = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)

contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
defect_output = crop.copy()

centers = []
for cnt in contours:
    x, y, w_box, h_box = cv2.boundingRect(cnt)
    if w_box == 0 or h_box == 0:
        continue
    cx = x + w_box//2
    cy = y + h_box//2
    centers.append((cx, cy))

for cnt in contours:
    area = cv2.contourArea(cnt)
    x, y, w_box, h_box = cv2.boundingRect(cnt)
    if w_box == 0 or h_box == 0:
        continue
    aspect_ratio = max(w_box/h_box, h_box/w_box)
    
    if 30 < area < 2000 and aspect_ratio < 5:
        if x > crop.shape[1] * 0.85:
            continue

        if y < crop.shape[0] * 0.35:
            continue
        
        cx = x + w_box//2
        cy = y + h_box//2

        
        neighbor_count = 0
        for (nx, ny) in centers:
            dist = np.sqrt((cx - nx)**2 + (cy - ny)**2)
            if dist < 35 and dist != 0:   
                neighbor_count += 1

        
        cluster_area = 0
        for cnt2 in contours:
            x2_c, y2_c, w2_c, h2_c = cv2.boundingRect(cnt2)
            cx2 = x2_c + w2_c//2
            cy2 = y2_c + h2_c//2
            dist2 = np.sqrt((cx - cx2)**2 + (cy - cy2)**2)
            if dist2 < 35:
                cluster_area += cv2.contourArea(cnt2)
     
        if neighbor_count > 2 or cluster_area > 300:
            continue
        pad_w = max(int(w_box * 5.0), 25)
        pad_h = max(int(h_box * 5.0), 25)
        x1 = max(x - pad_w, 0)
        y1 = max(y - pad_h, 0)
        x2 = min(x + w_box + pad_w, crop.shape[1]-1)
        y2 = min(y + h_box + pad_h, crop.shape[0]-1)
        cv2.rectangle(defect_output, (x1, y1), (x2, y2), (0,0,255), 2)
        cv2.putText(defect_output,f"defect",(x1,max(y1-5, 0)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

cv2.imshow("Edges ", edges)
#cv2.waitKey(0)
cv2.imshow("Defects Detected ", defect_output)
save_defect_path = os.path.join(save_dir, "belt_defects.bmp")
cv2.imwrite(save_defect_path, defect_output)
print("Defect detection saved:", save_defect_path)

cv2.waitKey(0)