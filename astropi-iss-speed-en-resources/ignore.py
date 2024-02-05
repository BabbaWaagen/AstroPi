from datetime import datetime
import cv2
import math
import exifread

def get_time(image_path):
    exif_data = get_exif_data(image_path)
    if exif_data is not None:
        time_str = exif_data.get('EXIF DateTimeOriginal')
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        return time
    else:
        print("Error: No EXIF data available.")
        return None

def get_time_difference(image_path_1, image_path_2):
    time_1 = get_time(image_path_1)
    time_2 = get_time(image_path_2)
    if time_1 is not None and time_2 is not None:
        time_difference = time_2 - time_1
        return time_difference.seconds
    else:
        return None

def convert_to_cv(image_path_1, image_path_2):
    image_1_cv = cv2.imread(image_path_1, 0)
    image_2_cv = cv2.imread(image_path_2, 0)
    return image_1_cv, image_2_cv


def calculate_features(image_1_cv, image_2_cv, feature_number):
    sift = cv2.SIFT_create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = sift.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):
    flann_index_kdtree = 0
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.5 * n.distance:
            good_matches.append(m)

    return good_matches

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    if matches:
        match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
        resize = cv2.resize(match_img, (1600, 600), interpolation=cv2.INTER_AREA)
        cv2.imshow("Matches:", resize)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def get_exif_data(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            exif_data = exifread.process_file(image_file)
            return exif_data
    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return None

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = [(keypoints_1[match.queryIdx].pt) for match in matches]
    coordinates_2 = [(keypoints_2[match.trainIdx].pt) for match in matches]
    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    distances = [math.hypot(x1 - x2, y1 - y2) for ((x1, y1), (x2, y2)) in zip(coordinates_1, coordinates_2)]
    return sum(distances) / len(distances) if distances else 0

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference if time_difference != 0 else 0
    return speed

if __name__ == "__main__":
    imagenum = 0

    while True:
        imagenum += 1
        imagenum2 = imagenum + 1

        image_path_1 = f'photo_{imagenum}.jpg'
        image_path_2 = f'photo_{imagenum2}.jpg'

        try:
            time_difference = get_time_difference(image_path_1, image_path_2)
            image_1_cv, image_2_cv = convert_to_cv(image_path_1, image_path_2)
            keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
            matches = calculate_matches(descriptors_1, descriptors_2)
            display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
            coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
            average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
            speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)

            print(f"Approximately: {speed} kmps")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            break  # Break out of the loop if the file is not found

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()  # Dies wird den vollständigen Traceback anzeigen
