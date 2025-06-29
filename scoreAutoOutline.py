'''
This sctipt runs with python 3.13
'''

if __name__ == "__main__":
    from template import computeOutline
    import pathlib
    import json
    import random
import time

    statistics=[]

    pictures_dirs = [pathlib.Path('pictures_rr'), pathlib.Path('pictures_other')]
    for pictures_dir in pictures_dirs:
        picture_files = [f for f in pictures_dir.rglob('*') if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.gif')]

        for picture in picture_files:
            #open corresponding .oln file
            # Assuming the .old file has the same name as the picture but with a different extension
            oln_file = picture.with_suffix('.oln')

            #read oln file as json
            with open(oln_file, 'r') as file:
                data = json.load(file)
            # Extract center_x, center_y, radius_x, radius_y from the json data
            center_x = data['outside_outline']['center_x']
            center_y = data['outside_outline']['center_y']
            radius_x = data['outside_outline']['radius_x']

            circleRadiusApproximate = radius_x * random.uniform(0.97, 1.03)  # Randomize radius by +/-3%
            with open(picture, 'rb') as img_file:
                pictures_rr = img_file.read()

            
            start_time = time.process_time()
            radius, center = computeOutline(pictures_rr, circleRadiusApproximate)
            elapsed_time = time.process_time() - start_time

            # compare center with centex_x and center_y from the json file
            radiusErrorPercent = abs(radius - radius_x)/ radius_x * 100
            centerErrorXPercent = abs(center[0] - center_x) / center_x * 100
            centerErrorYPercent = abs(center[1] - center_y) / center_y * 100
            #print(f"{picture.name}, Computed Radius: {radius}, Center: {center}, {radiusErrorPercent:.2f}% radius error, {centerErrorXPercent:.2f}% center X error, {centerErrorYPercent:.2f}% center Y error")
            statistics.append([ picture.name, radius, center[0], center[1], radiusErrorPercent, centerErrorXPercent, centerErrorYPercent, elapsed_time])


    print("Picture Name, Computed Radius, CenterX, CenterY, Radius Error Percent, Center X Error Percent, Center Y Error Percent, elapsed_time")
    for stat in statistics:
        print(f"{stat[0]}, {stat[1]}, {stat[2]}, {stat[3]}, {stat[4]:.2f}%, {stat[5]:.2f}%, {stat[6]:.2f}%, {stat[7]:.4f} seconds")   
    mean_radius_error = sum(stat[4] for stat in statistics) / len(statistics)
    mean_center_x_error = sum(stat[5] for stat in statistics) / len(statistics)
    mean_center_y_error = sum(stat[6] for stat in statistics) / len(statistics)
    mean_elapsed_time = sum(stat[7] for stat in statistics) / len(statistics)

    print("------------------------")
    print(f"Mean Radius Error: {mean_radius_error:.2f}%")
    print(f"Mean Center X Error: {mean_center_x_error:.2f}%")
    print(f"Mean Center Y Error: {mean_center_y_error:.2f}%")
    print(f"Mean Elapsed Time: {mean_elapsed_time:.4f} seconds")