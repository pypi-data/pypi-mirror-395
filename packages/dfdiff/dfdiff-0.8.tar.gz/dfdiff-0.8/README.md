# Overview
dfdiff is a Python Pyinstaller standalone executable with an accompanying Pythonlibrary that assist users with the task of gathering information about the differences between two CSV files using the Python Pandas library.

dfdiff takes two data files and a join key as input then identifies table variances between two files. The list of identified variances are as follow:
1. Field/column differences
2. Cell/data differences
3. Row/record differences
4. Whether if the join key produces duplicated joins

dfdiff provides the above output using Pandas DataFrame that can be further anlayzed or manipulated subsequently.

There are two primary methods of utilizing dfdiff geared toward different needs
* **Standalone executable (Windows 11)**: Designed for people who just want to get going with their analysis and cannot be bothered with seting up development and dealing with programming
* **Pandas library**: Designed for developers who would like finer control of the comparison process

# TL;DR Just Get Me Started Standalone Executable (Windows 11)
1. Downlaod [this file](https://github.com/andychien009/dfdiff/raw/refs/heads/main/release/win11/dfdiff.exe).
2. Place in directory
3. Open PowerShell and use the following command (if you are inputting everything in one line you can ignore the backtick "`" they are there for visual aesthetics
~~~
cd "<yourDirectory>"

.\dfdiff.exe --files <yourLeft.csv> <yourRight.csv> `
    --key "<yourKey1>" "<yourKey2>" `
    --outxlsx
~~~
4. Open result and see

# Table of Content
1. [Overview](#overview)
2. [TL;DR Just Get Me Started Standalone Executable (Windows 11)](#tldr-just-get-me-started-standalone-executable-windows-11)
3. [Standalone Executable (Windows 11)](#standalone-executable-windows-11)
4. [Using dfdiff Library](#using-dfdiff-library)
5. [Interpreting the Outputs](#interpreting-the-outputs)
   1. [Column/Field Differences (fdiff)](#columnfield-differences-fdiff)
   2. [Cell/Data Differences (cdiff)](#celldata-differences-cdiff)
   3. [Row/Record Level Differences (recdiff)](#rowrecord-level-differences-recdiff)
   4. [Duplicated Join Key (dupkey)](#duplicated-join-key-dupkey)
6. [About Me](#about-me)
7. [Dedication](#dedication)

# Standalone Executable (Windows 11)
There is no dependency or pre-requisit when it comes to using the standalone executable.

Please note, the currently available executable is built specifically for Windows 11 environment, should you need executable in other operating system if this build does not work for you, you will need to build your own executable or use the library version.

To use dfdiff standalone simply download the executable at [link](https://github.com/andychien009/dfdiff/raw/refs/heads/main/release/win11/dfdiff.exe).

Place dfdiff in any folder and navigate to it

```
# change the following to the working directory
cd c:\user\me\Documents\

# please note the ".\" prefixing the dfdiff.exe is significant if 
# you do not have your current working directory as part of the PATH
.\dfiff.exe --help

# you should be greeted with the following
usage: dfdiff [-h] --files FILE FILE --key KEY [KEY ...] [--outcsv] [--outxlsx] [--encoding ENC ENC]
              [--separators SEP SEP] [--version]

This program load two CSV files as string into Python Pandas DataFrame to identify the differences. Version 0.8. This
program is released under GPLv3 License. Written by Andy Chien andy_chien@hotmail.com -JAJA

options:
  -h, --help            show this help message and exit
  --files FILE FILE     The path to the left and right csv file
  --key KEY [KEY ...]   The list of join key to be used for joining the left and right table/csv. Composite key is
                        supported, separated by space and enclosed by double quote if necessary.
  --outcsv              The output of the diff file using CSV file. This output method maybe preferred if the XLSX
                        output experiences performance issues due to the size of the output data.
  --outxlsx             The output of the diff file. This output method is good for Excel-ready analysis, however it
                        may experience performance issue as output size grow. Try --outcsv if the program takes too
                        long to output.
  --encoding ENC ENC    (optional) Encoding for the left and right csv
  --separators SEP SEP  (optional) Separator for the left and right csv, use 't' for tab delimited file. Note that
                        there may be differences reading in mixed tab separated file with regular csv file due to
                        differences between pandas.read_table() and pandas.read_csv()
  --version             show program's version number and exit
```

We are ready to start at this point.

1. Place the two csv files you wish to compare in the folder
2. At minimum supply the following parameters
  * **--files file1.csv file2.csv** point the program to the files you wish to compare. File1 will be referred to as the *LEFT* file and file2 will be referred to as the *RIGHT* file.
  * **--key field1 field2 ...** the join key for the two files above separated by space. It is not necessary to use the primary key of the field if there is none, however choosing primary key for the two tables will ensure exact result without further manual analysis. If you have special characters or spaces in your field enclose it with double quotes
  * A method of ouput either **--outxlsx** or **--outcsv**
    *  **--outxlsx** outputs results to *<file2name>.xlsx* file. As with all Excel based output, it scales poorly with the size of the observed differences. Should this output method yield poor result, consider using the **--outcsv** option instead.
    *  **--outcsv** outputs a file using *<file2name>-tables.csv* will produce up to 4 different tables depending on the analysis.
3. Optionally you may use the following to alter the loading behaviors
  * **--separators f1sep f2sep** by default, the program assumes a csv is supplied with the default separator as ",". Should this be different specify it here. Use "t" for tab limited file, but note that tab delimited files are read in using pandas.read_table() instead of pandas.read_csv() and may cause minor differences.
  * **--encoding f1enc f2enc** by default, the program read data in using 'latin1' as the primary encoding adjust it here

The program will do the following, read the two files in as table of string only (with no interpretation of values, or datatype) using specifciation provided. It will make attempt to join the two tables using the join key supplied and perform comparison operations.

Depending on the output option selected it will either output as a CSV or Excel file. If output option is specified, the program will simply output a summary of variances on the console. If the program completes with no ouput in the console it means that no differences between the two files are observed.

The program outputs 4 different types of tables. See [Interpreting the Outputs](#interpreting-the-outputs) for more information.

# Using dfdiff Library
The benefit of using the dfdiff library is that the programmer will be able to assert more control around (entering and exiting) the comparison process. Following are some use cases that may warrant looking into using the dfdiff library instead of the standalone executable
* To load the data using conditions that are not covered by the standalone executable options. Even though all variables are loaded as string for the comparison, some more adventurous programmer may choose to have Pandas automatically detect data types (even though that is more likely yield unexpected result) or manually specified data format.
* If the join key need to be processed prior to the join. For example zero padding the join key, a situation commonly happens after opening the CSV in Excel causing discrepancy to the source data.
* To pre-eliminate or remove false positive difference results. For example in the case of "1.0" vs "1" either the data could be adjusted so that the display format for the fields are equivalent before the comparison step or the data could be filtered out from the comparison step.
* If other output formats other than the out-of-the-box **--outxlsx** and **--outcsv** formats are desired.

The dfdiff Python library is readily available in Pypi and can be installed through the usual pip installation process.

You will need to install the library and its necessary dependencies

```
pip install pandas numpy openpyxl dfdiff
```

An example skeleton program with information about the invocation and the use is as follow.

```
import pandas as pd

from dfdiff.dfdiff import dfdiff

F1="left.csv"
F2="right.csv"

with open(F1, 'r', encoding='latin_1') as F:
    left = pd.read_csv(F)

with open(F2, 'r', encoding='latin_1') as F:
    right = pd.read_csv(F)
   
# suppose we want to pad 0 in the id before we start comparison
left['id'] = left['id'].str.pad("0", side="left", fillchar="0")

cmp = dfdiff(left, right, uargs.pkey)
fdiff, cdiff, recdiff, dupkey = cmp.getDiffDfs()

# .... rest of the program
```

dfdiff library outputs 4 different types of tables in Pandas.DataFrame format ready for further processing in the exact sequence after invoking the `dfdiff.getDiffDfs()`. 

1. fdiff
2. cdiff
3. recdiff
4. dupkey

If you have no use for a specific diff dataframe use Python's single underscore `_` to ignore the value.

```
# the following will register only the cell diff and rec diff
# dataframe
_, cdiff, recdiff, _ = cmp.getDiffDfs()
```

See [Interpreting the Outputs](#interpreting-the-outputs) for more information.

# Interpreting the Outputs
## Column/Field Differences (fdiff)
The program outputs a table that highlight the field differences between the left and the right file. It will have the following columns.

This will either be in the *[fielddiff]* sheet in Excel or the *file2name-fdiff.csv* file.

| Column Name       | Description                                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------------------------|
| l_ordinalposition | The ordinal position of the fields of the tables to the left                                                    |
| l_fname           | The field name of the left file                                                                                 |
| r_fname           | The field name of the right file                                                                                |
| r_ordinalposition | The ordinal position of the fields of the table to the right. The table will sort using this column by default. |
| _merge            | Hint for field in question whether if it is availalbe only in the 'left', 'right', or 'both'                    |

## Cell/Data Differences (cdiff)
At this section, the program compares the string value of the left and right table and identify the differences.

The output includes the keys used to identify the row (primary key if that is what was supplied) at the start of the column, then the field name where the variance is observed, then the left and right value of the field.


| Column Name              | Description                                                                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------------------|
| join keys (multi columns) | The join key supplied to identify unique row/record                                                            |
| fname                    | The field/column name where the variance is observed                                                           |
| lval                     | The value from the left table identified by the combination of the join key as well as the field name (fname)  |
| rval                     | The value from the right table identified by the combination of the join key as well as the field name (fname) |

It is important to note that the dfdiff executable reads everything in as string value with no interpretation; this means the value "1.0" and "1" will be identified as a differences regardless of the value. This is by design to simplify the programming. Should you wish to exclude such fals positive variances, either perform further manual analysis from the output or implement your own screening through the dfdiff library.

## Row/Record Level Differences (recdiff)
The next section highlight the row/record level differences observed by the dfdiff program/library. 

Notionally this highlight the variances of rows/records between the two datasets.

The output contains key to identify the record that is missing and the flag **exists** to indicate which table the record exists but not the other table.


| Column Name               | Description                                                                                                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| join keys (multi-columns) | The join key supplied to identify unique row/record                                                                                                                              |
| exits                     | Contains the value 'L' or 'R' depending on where the record identified by the join key currently exists. The record marked by the join key will be missing from the other table. |

## Duplicated Join Key (dupkey)
When joining the left and the right table, dfdiff makes attempt to analyze the join key and do its best to ensure that there is a one-to-one join; as that is what makes the concept of a table diff makes sense.

However in real life or data that are currently under development it may not be the case. The program idenfies join keys that have yielded one-to-many or many-to-many join which could be problematic for the aanalysis of table difference.

Due to the nature of the join, there will no reliable method to programmatically identify the table differences. Records with these key will have to be manually assessed for their integrity and differences. It is also important to note the tables earlier do not have these results excluded. Instead, dfdiff completes the one-to-many and many-to-many join and assess the differences mentioned above regardless of the complication identified by this step.

| Column Name               | Description                                                                                              |
|---------------------------|----------------------------------------------------------------------------------------------------------|
| join keys (multi-columns) | The join key supplied to identify unique row/record                                                      |
| count                     | The count of the number of duplication the supplied join key took place in the dataset                   |
| exits                     | Contains the value 'L' or 'R' depending on where the record identified by the join key currently exists. |


# About Me
My name is Hsiang-An (Andy) Chien. Currently, full-time ETL Engineer and Business Intelligence Solution Developer (the title changes so fast these days), part-time general computing and gaming enthusiast.

I would love to hear about my work being used to tackle common challenges others may have encountered along their way. Share this program and library with others who may need it.

If you have success story to tell, it would make my day! Message me at andy_chien (at) hotmail.com.

# Dedication
I dedicate this work, a piece of me, for the world and for my loving family: Jina Chiang, Julia, and Alison Chien. I hope that a piece of me will be around and kicking on the interweb watching over you through time.
