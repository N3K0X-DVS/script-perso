# **CSV-Nexus Shell**

CSV-Nexus Shell is a Python-based interactive command-line application for managing, viewing, sorting, and merging CSV datasets. The tool is designed to simplify the process of working with tabular data files.

---

## **Features**
- **Merge CSV Files**: Combine multiple CSV files into a single dataset, provided the headers match.
- **View Dataset**: Display the current dataset in a well-aligned, human-readable format.
- **Sort Dataset**: Sort the dataset based on any column, with optional reverse sorting.
- **Export Dataset**: Save the current dataset to a new CSV file.

---

## **Setup Instructions**

### **1. Prerequisites**
Download the executable
### **2. Preparing the Environment**
Place the script (`csv_nexus.exe`) and any CSV files you want to work with in the same directory.

### **3. Running the Script**
Run the script in a terminal or command prompt:

```bash
csv_nexus
```

---

## **Usage Guide**

Once the script is running, you will see a prompt: `CSV-Nexus:`. From here, you can use the following commands:

### **1. Exit the Shell**
**Command**: `exit`  
**Description**: Exits the CSV-Nexus Shell.  
**Example**:
```bash
CSV-Nexus: exit
```

---

### **2. Add a CSV File**
**Command**: `add`  
**Description**: Lists available CSV files in the current directory and merges the selected file into the current dataset. The headers of the new file must match the existing dataset.  
**Example**:
```bash
CSV-Nexus: add
```
- Select a file by entering its number from the displayed list.

---

### **3. View the Current Dataset**
**Command**: `view`  
**Description**: Displays the current dataset in an aligned, tabular format for easy readability.  
**Example**:
```bash
CSV-Nexus: view
```

---

### **4. Sort the Dataset**
**Command**: `sort`  
**Description**: Sorts the dataset by a specified column. You will be prompted to:
- Choose a column number.
- Decide if the sort should be in reverse order.

**Example**:
```bash
CSV-Nexus: sort
```

---

### **5. Export the Dataset**
**Command**: `export`  
**Description**: Exports the current dataset to a new CSV file. You will be prompted to provide a filename.  
**Example**:
```bash
CSV-Nexus: export
Name of the file to export: sorted_data.csv
```

---

## **File Structure**
The application relies on a supporting library (`lib.py`) to handle CSV operations. This file should include:
- `load_csv(file_path)`: Function to read a CSV file and return its header and data.
- `equality_check(header1, header2)`: Function to verify if two headers match.
- `sort_data(data, header, column, reverse)`: Function to sort data by a specified column.
- `write_csv(file_name, data, header)`: Function to write the dataset to a CSV file.

Ensure `lib.py` is in the same directory as `csv_nexus_shell.py`.

---

## **Error Handling**
- **Header Mismatch**: If the headers of a new CSV file do not match the current dataset, an error will be raised.
- **Invalid Input**: The shell prompts for numeric input when necessary and validates it.

---

## **Examples**

### Example: Adding and Viewing a CSV File
```bash
CSV-Nexus: add
1. data1.csv
2. data2.csv
Number of the file to add: 1
CSV-Nexus: view
Name                 | Value1     | Value2     | Category       | Tag       
---------------------------------------------------------------------------
Pommes               | 50.0       | 0.5        | Fruits         | sante     
Oranges              | 85.0       | 0.58       | Fruits         | sante     
```

### Example: Sorting the Dataset
```bash
CSV-Nexus: sort
1. Name
2. Value1
3. Value2
4. Category
5. Tag
Number of the column to sort: 2
reverse the sort ?(y/n): n
CSV-Nexus: view

Name                 | Value1     | Value2     | Category       | Tag       
---------------------------------------------------------------------------
Oranges              | 85.0       | 0.58       | Fruits         | sante     
Pommes               | 50.0       | 0.5        | Fruits         | sante     
```
