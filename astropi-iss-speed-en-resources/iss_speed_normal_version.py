from picamera import PiCamera
from time import sleep
from datetime import datetime
import cv2
import math
from exif import Image

##########################
######## Made by #########
###### BabbaWaagen #######
########## And ###########
######  DeMika69 #########
##########################


# Initialize the PiCamera and set its resolution
camera = PiCamera()
camera.resolution = (4056, 3040)  # Set camera resolution to (4056, 3040)

# Helper function to take photos
def take_photo(filename):
    camera.start_preview()  # Start the camera preview
    sleep(2)  # Warm-up time for the camera
    camera.capture(filename)  # Capture the image and save it
    camera.stop_preview()  # Stop the camera preview

# Extracts the original datetime from the image's EXIF data
def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        # Fallback to current datetime if no EXIF datetime found
        time_str = img.get("datetime_original", datetime.now().strftime('%Y:%m:%d %H:%M:%S'))
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        return time

# Calculates the time difference in seconds between two images
def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

# Converts images to grayscale for OpenCV processing
def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)  # Read and convert image to grayscale
    image_2_cv = cv2.imread(image_2, 0)  # Read and convert image to grayscale
    return image_1_cv, image_2_cv

# Calculates keypoints and descriptors using SIFT algorithm
def calculate_features(image_1_cv, image_2_cv, feature_number):
    sift = cv2.SIFT_create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = sift.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

# Matches features between two images using FLANN based matcher
def calculate_matches(descriptors_1, descriptors_2):
    flann_index_kdtree = 0
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
    # Filter for good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    return good_matches

# Displays the best matches between two images
def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = matches[:int(len(matches) * 0.8)]  # Display only the best 80% of matches
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, good_matches, None)
    resize = cv2.resize(match_img, (1600, 600), interpolation=cv2.INTER_AREA)
    cv2.imshow("Matches", resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Finds matching coordinates between two sets of keypoints
def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1, y1) = keypoints_1[image_1_idx].pt
        (x2, y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1, y1))
        coordinates_2.append((x2, y2))
    return coordinates_1, coordinates_2

# Calculates the mean distance between matching coordinates
def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances += distance
    return all_distances / len(merged_coordinates)

# Calculates the speed of the observed changes in kmps
def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000  # Convert to kilometers
    speed = distance / time_difference  # Speed in kilometers per second
    return speed

# Main loop to continuously take photos and estimate speed
while True:
    filename1 = 'image1.jpg'
    filename2 = 'image2.jpg'

    take_photo(filename1)
    sleep(10)  # Wait for 10 seconds before taking the next photo
    take_photo(filename2)

    # Speed calculation using the two most recent photos
    time_difference = get_time_difference(filename1, filename2)
    image_1_cv, image_2_cv = convert_to_cv(filename1, filename2)
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)

    print(f"Approximately:  {round(speed,2)} kmps")
