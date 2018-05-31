# Text Detection

Given a store tag, generate an educated guess about what product might be.\
Currently only looking for productName. This will be changed to look for productCategory, UPC, and brand as well once the database server is up.\



## Installation
Install everything inside of requirements.txt (contains the EAST requirements as well)\

Install Tesseract\
  https://github.com/tesseract-ocr/tesseract\

Install fuzzywuzzy c binaries (Optional but will decrease runtime by a factor of 4)\
  Look at https://github.com/seatgeek/fuzzywuzzy for c binaries\


## Usage

Usage: Refer to comments above each method\
dbFile should be a csv formatted in the same way as montrealUPCs.csvFile.\



## History

May 24: V0.0: works only with product names and uses CSV input\
May 31: V1.0: included support for text detection schemes\
