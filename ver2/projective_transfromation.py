# Installed Packages
import numpy as np

# Standard Packages
import argparse
import time

# Original Sources
import util.area as area
from util.setup import load_settings, set_up_cap, set_up_csv_one_path
from util.csv import load_target_csv


def main(config_path):
  start = time.perf_counter()

  # Load Settings
  config = load_settings(config_path)
  video_path = config['video_path']
  csv_path = config['target_area_points_output_path']
  target_vertical = config['projective_transform_point_vertical']
  target_horizontal = config['projective_transform_point_horizontal']
  expect_area_output_path = config['expect_area_output_path']

  cap = set_up_cap(video_path)
  set_up_csv_one_path(expect_area_output_path)

  ret, frame = cap.read()
  if not ret:
    raise Exception("Frame could not be loaded successfully.")
  
  area_manager = area.Area(frame)

  road_points_data = load_target_csv(csv_path)
  target_points = [target_vertical, target_horizontal]

  pf_points = area_manager.applyProjectiveTransform(target_points, road_points_data)

  rectangle_area = area_manager.calcArea(pf_points)

  np.savetxt(expect_area_output_path, np.array([rectangle_area]), delimiter=',', fmt='%f')

  print(f'Rectangle Area: {rectangle_area}')

  end = time.perf_counter()

  print(f"実行時間: {end - start:.2f}s")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)