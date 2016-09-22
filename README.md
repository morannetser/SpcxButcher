# The SPCX Butcher
![alt tag](https://raw.githubusercontent.com/morannetser/SpcxButcher/master/butcher_knife.png)

This project is an SPCX parsing library.

Why call it SpcxButcher?

Well, we love photons. SPCX files? not so much. After some experience with the SPCX format we decided that _parsing_ them would be too lenient. 

**WE DECIDED TO BUTCHER THEM INSTEAD**!!

## Python 3

SPCX Butcher uses Python 3. We did not test it using Python 2

## Coverting SPCX files to MATLAB format

The following will take an SPCX file and produce many `*.mat` files, one per SPC. E.g.:

    $ python3 tools/spcx_to_matlab.py data/example.spcx data/some_prefix

will produce `some_prefix.0.mat, some_prefix.1.mat, some_prefix.2.mat,...` in the `data` directory.

## Coverting SPCX files to JSON format

The following will take an SPCX file and write a JSON representation of it to `stdout`.  

    $ python3 tools/spcx_to_json.py fixtures/small.spcx 
    {"spcs": [{"events": [[0, 3, 47638]], "raw": 0, "timePerBin": 164610}, {"events": [[0, 6, 42779], [0, 6, 47325]], "raw": 0, "timePerBin": 164610}, {"events": [[0, 2, 47560], [0, 9, 47947], [0, 5, 48175]], "raw": 0, "timePerBin": 164610}]}

## Using SPCX Butcher from your Python program

```python
import spcxbutcher.spcxparser

parsed = spcxbutcher.spcxparser.SPCXParser( 'some_file.spcx' )
for spc in parsed:
    for event in spc:
        print( event.timestamp, event.channel )
```
