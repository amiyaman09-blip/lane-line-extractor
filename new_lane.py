import os
import cv2
import numpy as np

IMAGES = [
    {
        "path": "image/new image.jpeg",
        "roi": [(0, 1), (0, 0.82), (0.47, 0.61), (0.53, 0.61), (1, 0.82), (1, 1)],
    },
    {
        "path": "image/image2.png",
        "roi": [(0, 1), (0, 0.80), (0.27, 0.44), (0.40, 0.43),
                (0.62, 0.50), (0.80, 0.60), (0.93, 0.76), (0.93, 1)],
    },
]

SHOW_WINDOWS = False
MIN_COMPONENT_AREA = 80   # Lowered to capture thinner line fragments in perspective distance
MIN_VERTICAL_EXTENT = 0.10

NUM_WINDOWS = 35          # Increased windows to track tighter step sections smoothly
WINDOW_MARGIN = 45        

# Keep yellow threshold standard as its hue remains consistent
YELLOW_LOW, YELLOW_HIGH = (14, 50, 90), (36, 255, 255)

DRAW_COLOURS = {"white": (0, 0, 255), "yellow": (255, 0, 0)}
INFLECTION_COLOUR = (0, 255, 0)


def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise SystemExit(f"Error: Could not load {path}. Check that the image exists.")
    return cv2.resize(image, (960, 540))


def roi_polygon(width, height, points):
    return np.array([[(int(x * (width - 1)), int(y * (height - 1))) for x, y in points]],
                    dtype=np.int32)


def extract_adaptive_masks(image):
    """Uses adaptive thresholding to extract lane markings under varying shadows."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Adaptive threshold isolates localized contrast changes (perfect for shadows)
    adaptive_white = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 51, -15
    )
    
    # Filter yellow using standard HSV hue ranges
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, np.array(YELLOW_LOW), np.array(YELLOW_HIGH))
    
    # Clean up the white mask by removing known non-white properties
    # This prevents the adaptive threshold from catching dark roadside foliage borders
    blur_v = hsv[:, :, 2]
    refined_white = cv2.bitwise_and(adaptive_white, adaptive_white, mask=cv2.inRange(blur_v, 110, 255))
    
    return refined_white, yellow


def apply_roi(mask, roi):
    roi_mask = np.zeros_like(mask)
    cv2.fillPoly(roi_mask, roi, 255)
    return cv2.bitwise_and(mask, roi_mask)


def detect_edges(image, roi):
    white, yellow = extract_adaptive_masks(image)
    colour_mask = cv2.bitwise_or(white, yellow)
    blurred = cv2.GaussianBlur(colour_mask, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 100)
    roi_edges = apply_roi(edges, roi)
    return white, yellow, colour_mask, blurred, edges, roi_edges


def trace_lane_windows(component_mask):
    ys, xs = np.nonzero(component_mask)
    if len(ys) == 0:
        return None

    y_max, y_min = ys.max(), ys.min()
    
    starting_indices = ys > (y_max - 15)
    if not np.any(starting_indices):
        return None
    current_x = xs[starting_indices].mean()

    window_height = int((y_max - y_min) / NUM_WINDOWS)
    if window_height < 2:
        return None

    traced_points = []
    last_dx = 0  

    for w in range(NUM_WINDOWS):
        win_y_low = y_max - (w + 1) * window_height
        win_y_high = y_max - w * window_height
        
        win_indices = ((ys >= win_y_low) & (ys < win_y_high) & 
                       (xs >= current_x - WINDOW_MARGIN) & (xs <= current_x + WINDOW_MARGIN))
        
        if np.any(win_indices):
            new_x = xs[win_indices].mean()
            
            if w > 0 and len(traced_points) > 0:
                expected_x = current_x + last_dx
                current_x = 0.70 * new_x + 0.30 * expected_x
                last_dx = current_x - traced_points[-1][0]
            else:
                current_x = new_x
                
            mean_y = (win_y_low + win_y_high) / 2.0
            traced_points.append((current_x, mean_y))
        else:
            if w > 0 and len(traced_points) > 0:
                current_x = current_x + last_dx
                mean_y = (win_y_low + win_y_high) / 2.0
                traced_points.append((current_x, mean_y))

    if len(traced_points) < 5:
        return None

    return np.array(traced_points[::-1])


def find_discrete_inflection(points):
    if len(points) < 8:
        return None

    xs = points[:, 0]
    ys = points[:, 1]

    dx = np.diff(xs)
    dy = np.diff(ys)
    
    dy[dy == 0] = 1e-5 
    first_deriv = dx / dy
    
    second_deriv = np.diff(first_deriv) / dy[:-1]

    if len(second_deriv) >= 5:
        second_deriv = np.convolve(second_deriv, np.ones(5)/5, mode='same')

    sign_changes = np.where(np.diff(np.sign(second_deriv)))
    
    if len(sign_changes) == 0 or len(sign_changes[0]) == 0:
        return None
        
    target_idx = int(sign_changes[0][len(sign_changes[0]) // 2]) + 2
    
    if target_idx < len(points):
        return int(round(points[target_idx, 0])), int(round(points[target_idx, 1]))
    return None


def detect_lanes(image, masks, roi):
    height, width = image.shape[:2]
    result = image.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    found = 0

    for name, mask in masks.items():
        mask = apply_roi(mask, roi)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        for i in range(1, count):
            area = stats[i, cv2.CC_STAT_AREA]
            extent = stats[i, cv2.CC_STAT_HEIGHT] / height
            if area < MIN_COMPONENT_AREA or extent < MIN_VERTICAL_EXTENT:
                continue

            curve_points = trace_lane_windows((labels == i).astype(np.uint8))
            if curve_points is None:
                continue

            formatted_points = curve_points.astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(result, [formatted_points], False, DRAW_COLOURS[name], 4)
            found += 1

            bend = find_discrete_inflection(curve_points)
            if bend is not None:
                cv2.circle(result, bend, 9, INFLECTION_COLOUR, -1)
                cv2.circle(result, bend, 9, (0, 0, 0), 2)

    if found == 0:
        print("No lane lines detected. Check the ROI and colour masks.")
    return result


def process_image(config):
    path = config["path"]
    name = os.path.splitext(os.path.basename(path))[0].replace(" ", "_")
    folder = os.path.join("output", name)
    os.makedirs(folder, exist_ok=True)

    image = load_image(path)
    height, width = image.shape[:2]
    roi = roi_polygon(width, height, config["roi"])

    white, yellow, colour_mask, blurred, edges, roi_edges = detect_edges(image, roi)
    lane_image = detect_lanes(image, {"white": white, "yellow": yellow}, roi)

    roi_preview = image.copy()
    cv2.polylines(roi_preview, roi, True, (0, 255, 0), 2)

    cv2.imwrite(f"{folder}/colour_mask.jpg", colour_mask)
    cv2.imwrite(f"{folder}/blurred.jpg", blurred)
    cv2.imwrite(f"{folder}/canny_edges.jpg", edges)
    cv2.imwrite(f"{folder}/roi_edges.jpg", roi_edges)
    cv2.imwrite(f"{folder}/roi_preview.jpg", roi_preview)
    cv2.imwrite(f"{folder}/lane_lines.jpg", lane_image)
    print(f"Processed {path} -> {folder}")

    if SHOW_WINDOWS:
        for title, img in [("Original", image), ("Colour Mask", colour_mask),
                           ("Blurred", blurred), ("Canny Edges", edges),
                           ("ROI Edges", roi_edges), ("ROI Preview", roi_preview),
                           ("Detected Lane Lines", lane_image)]:
            cv2.imshow(f"{name} - {title}", img)


def main():
    for config in IMAGES:
        process_image(config)

    if SHOW_WINDOWS:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()







