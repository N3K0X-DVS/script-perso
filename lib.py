

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