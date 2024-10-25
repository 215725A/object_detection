import csv

def load_target_csv(csv_path):
  csv_datas = []
  with open(csv_path, encoding='utf8', newline='') as f:
    csv_reader = csv.reader(f)
    for csv_data in csv_reader:
      data = [int(c_data) for c_data in csv_data]
      csv_datas.append(data)
  
  return csv_datas

def load_ratio_csv(csv_path):
  csv_datas = []
  with open(csv_path, encoding='utf8', newline='') as f:
    csv_reader = csv.reader(f)
    for csv_data in csv_reader:
      data = [float(c_data) for c_data in csv_data]
      csv_datas.append(data)
  
  return csv_datas

def load_expect_area_csv(csv_path):
  csv_datas = []
  with open(csv_path, encoding='utf8', newline='') as f:
    csv_reader = csv.reader(f)
    for csv_data in csv_reader:
      data = [float(c_data) for c_data in csv_data]
      csv_datas.append(data)
  
  return csv_datas[0][0]