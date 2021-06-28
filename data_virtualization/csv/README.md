# Virtualization of CSV files through HDF5

## Description

Shows how to map a CSV file to HDF5. The input file is converted into a
compound dataset that can be inspected by existing HDF5 tools.

## Data preparation

Run the code below to obtain the parameters needed to create the UDF dataset.
The input file, [albumlist.csv](https://github.com/Currie32/500-Greatest-Albums),
is parsed to determine the compound member names and their data types. The
output dataset is named `GreatestAlbums` and the reference HDF5 file where
that dataset is stored is `reference.h5`.

```
import csv

def dataType(row):
    py2udf = {"int": "int32", "float": "float", "str": "string"}
    for guess in ["type(int(row)).__name__", "type(float(row)).__name__", "type(row).__name__"]:
        try:
            return py2udf[eval(guess)]
        except ValueError:
            pass
    return py2udf["str"]

with open("albumlist.csv", newline="") as f:
    hdf5_file = "reference.h5"
    udf_file = "udf-csv.py"
    udf_dataset = "GreatestAlbums"

    reader = csv.reader(f)
    header, data = next(reader), next(reader)
    members = ",".join([f"{header[i]}:{dataType(x)}" for i,x in enumerate(data)])
    print("hdf5-udf {} {} {}:{{{}}}:{}".format(
        hdf5_file, udf_file, udf_dataset, members, len([row for row in reader]) + 1))
```

Note that the string data type declared in the `py2udf` array does not have a
predefined sized (such as `string(64)`). By omitting the size, we instruct
HDF5-UDF to use the default size of 32 characters for each string read from
the input CSV file. Please adjust that size according to the input data you
intend to process.

## Data consumption

The UDF dataset can be read with standard tools like `h5dump`:

```
h5dump -d /GreatestAlbums reference.h5
```
