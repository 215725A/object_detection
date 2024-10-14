import csv

def load_csv(csv_path):
  csv_datas = []
  with open(csv_path, encoding='utf8', newline='') as f:
    csv_reader = csv.reader(f)
    for csv_data in csv_reader:
      data = [int(c_data) for c_data in csv_data]
      csv_datas.append(data)
  
  return csv_datas