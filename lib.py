import os
import csv


def equality_check(arr1: list[str], arr2: list[str]) -> bool:
   if len(arr1) != len(arr2):
      return False
   for i in range(0, len(arr2)):
      if arr1[i] != arr2[i]:
         return False
   return True


def load_csv(file: str, directory:str, delimiter: str=',') -> tuple[list[str], list[list[str]]]:
    if file not in os.listdir(directory):
        raise FileNotFoundError("csv file not in the directory")
    with open(os.path.join(directory, file), newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        temp = []
        for row in spamreader:
            temp.append(row)
        if not temp:
            raise ValueError("csv file empty")
        if len(temp[0]) != 4:
            raise ValueError("csv file must contain exactly 4 columns")
        if len(temp) < 2:
            raise ValueError("csv file must contain at least 1 header and 1 line of data")
        header = temp[:1][0]
        header.append('département')
        temp = temp[1:]
        data = []
        try:
            data += [[row[0], float(row[1]), float(row[2]), row[3], os.path.splitext(file)[0]] for row in temp]
        except ValueError:
            raise ValueError("Row contains invalid data types (expected str, float, float, str)")
        except IndexError:
            raise IndexError("Not enough rows in csv file")

        #print(header)
        return header, data

def write_csv(file: str, data: list[list[str]], header:list[str], directory:str, delimiter: str=',', force_overwrite: bool= False) -> None:
    #print(file in os.listdir('.'))
    if not force_overwrite:
        if file in os.listdir(directory):
            choix = None
            while choix != 'yes' and choix != 'n':
                choix = input('warning file exist, would you overwrite it ? (yes/n)')
            if choix == 'n':
                return

    with open(os.path.join(directory, file), 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter)
        csv_writer.writerow(header)
        csv_writer.writerows(data)

def sort_data(data, header, column, reverse: bool = False):
    if column in header:
        #print(header.index(column))
        data = sorted(data, key=lambda x: x[header.index(column)], reverse=reverse)
        #[print(row) for row in data]
    else:
        raise ValueError('the sort parameter don\'t match a column')

    return data