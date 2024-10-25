# Installed Packages
import cv2
import numpy as np

# Standard Packages
import argparse
import time

# Original Sources
import util.area as area
from util.setup import load_settings, set_up_cap, set_up_csv


def main(config_path):
  start = time.perf_counter()

  # Load Settings
  config = load_settings(config_path)
  video_path = config['video_path']
  csv_paths = [config['target_area_points_output_path'], config['aspect_ratio_output_path']]
  expect_vertical = config['projective_transform_point_vertical']
  expect_horizontal = config['projective_transform_point_horizontal']
  expect_distances = [expect_vertical, expect_horizontal]

  set_up_csv(csv_paths)

  target_area_points_output_path = config['target_area_points_output_path']
  aspect_ratio_output_path = config['aspect_ratio_output_path']

  cap = set_up_cap(video_path)

  ret, frame = cap.read()
  if not ret:
    raise Exception("Frame could not be loaded successfully.")
  
  area_manager = area.Area(frame)

  display_img = area_manager.drawArea()

  cv2.imshow('DrawAreaImage', display_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  # save csv files
  target_points = np.array(area_manager.point_list)
  np.savetxt(target_area_points_output_path, target_points, delimiter=',', fmt='%d')

  ratios = area_manager.calcAspectRatio(expect_distances)
  np.savetxt(aspect_ratio_output_path, ratios, delimiter=',', fmt='%.2f')

  cap.release()

  end = time.perf_counter()

  print(f"実行時間: {end - start:.2f}s")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)