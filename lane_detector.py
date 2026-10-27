import os
import cv2
import numpy as np

IMAGE_PATH = "images/road.png"
SHOW_WINDOWS = False

HORIZON = 0.52


def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise SystemExit(f"Error: Could not load {path}. Check that the image exists.")
    return cv2.resize(image, (960, 540)), image


def roi_polygon(width, height):
    return np.array([[
        (0, height - 1),
        (0, int(height * 0.73)),
        (int(width * 0.46), int(height * HORIZON)),
        (int(width * 0.54), int(height * HORIZON)),
        (width - 1, int(height * 0.73)),
        (width - 1, height - 1),
    ]], dtype=np.int32)


def detect_edges(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    white_mask = cv2.inRange(hsv, np.array([0, 0, 190]), np.array([180, 40, 255]))
    yellow_mask = cv2.inRange(hsv, np.array([15, 80, 120]), np.array([35, 255, 255]))
    
    combined_mask = cv2.bitwise_or(white_mask, yellow_mask)
    blurred = cv2.GaussianBlur(combined_mask, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    height, width = edges.shape
    roi_mask = np.zeros_like(edges)
    cv2.fillPoly(roi_mask, roi_polygon(width, height), 255)
    roi_edges = cv2.bitwise_and(edges, roi_mask)

    return white_mask, yellow_mask, combined_mask, blurred, edges, roi_edges


def fit_lane(points, y_top, y_bottom):
    pts = np.array(points, dtype=np.float32)
    vx, vy, x0, y0 = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01).flatten()
    if abs(vy) < 1e-6:
        return None
    x_top = int(x0 + (y_top - y0) * vx / vy)
    x_bottom = int(x0 + (y_bottom - y0) * vx / vy)
    return (x_top, y_top), (x_bottom, y_bottom)


def detect_lanes(image, roi_edges):
    height, width = roi_edges.shape
    result = image.copy()

    lines = cv2.HoughLinesP(
        roi_edges, rho=1, theta=np.pi / 180,
        threshold=20, minLineLength=20, maxLineGap=40,
    )
    if lines is None:
        print("No lane segments detected. Check the ROI and colour mask.")
        return result

    left, right = [], []
    for x1, y1, x2, y2 in lines.reshape(-1, 4):
        dx, dy = int(x2 - x1), int(y2 - y1)
        if abs(dy) < 4:
            continue
        mx = (x1 + x2) / 2
        slope = dy / (dx if dx != 0 else 0.001)

        if -2.5 < slope < -0.2 and mx < 0.5 * width:
            left += [(x1, y1), (x2, y2)]
        elif 0.2 < slope < 2.5 and mx > 0.5 * width:
            right += [(x1, y1), (x2, y2)]

    y_top = int(height * HORIZON) + 5
    y_bottom = height - 1

    for pts in (left, right):
        if len(pts) < 4:
            continue
        seg = fit_lane(pts, y_top, y_bottom)
        if seg:
            cv2.line(result, seg[0], seg[1], (0, 0, 255), 4)

    return result


def outline_centre_dashes(image, full_image):
    full_h, full_w = full_image.shape[:2]
    scale = np.array([image.shape[1] / full_w, image.shape[0] / full_h])

    hsv = cv2.cvtColor(full_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 170]), np.array([180, 50, 255]))

    road = np.zeros_like(mask)
    cv2.fillPoly(road, roi_polygon(full_w, full_h), 255)
    mask = cv2.bitwise_and(mask, road)

    strip = np.zeros_like(mask)
    x0, x1 = int(full_w * 0.44), int(full_w * 0.54)
    strip[:, x0:x1] = mask[:, x0:x1]

    contours, _ = cv2.findContours(strip, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        if len(c) < 2:
            continue
        hull = cv2.convexHull(c)
        shape = np.round(hull.astype(np.float32) * scale).astype(np.int32)

        if cv2.contourArea(shape) < 40:
            cv2.fillPoly(image, [shape], (0, 0, 255))
            cv2.polylines(image, [shape], True, (0, 0, 255), 1)
        else:
            cv2.polylines(image, [shape], True, (0, 0, 255), 2)
    return image


def main():
    os.makedirs("output", exist_ok=True)
    
    image, full_image = load_image(IMAGE_PATH)
    white_mask, yellow_mask, combined_mask, blurred, edges, roi_edges = detect_edges(image)
    lane_image = detect_lanes(image, roi_edges)
    lane_image = outline_centre_dashes(lane_image, full_image)

    cv2.imwrite("output/original.jpg", image)
    cv2.imwrite("output/hsv_mask.jpg", white_mask)      
    cv2.imwrite("output/colour_mask.jpg", yellow_mask)  
    cv2.imwrite("output/blurred.jpg", blurred)
    cv2.imwrite("output/canny_edges.jpg", edges)
    cv2.imwrite("output/roi_edges.jpg", roi_edges)
    cv2.imwrite("output/lane_lines.jpg", lane_image)
    
    print("Processing complete. Check your output folder.")


if __name__ == "__main__":
    main()
