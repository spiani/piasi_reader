# Piasi_reader
A Python library to read the L1C IASI native files

This library offers a pythonic interface to read the data
produced by the IASI interferometers (in native format).

More information about the IASI interferometers and
their data can be found at the following web page:
<https://navigator.eumetsat.int/product/EO:EUM:DAT:0101>

## Installation

Clone this repository with the following command:

```
git clone git@github.com:spiani/piasi_reader.git
```

and then run the install script

```
cd piasi_reader
python setup.py install
```

## Usage
Import the library

```
from piasi_reader.iasi_l1c_native_file import IasiL1cNativeFile
```

From there, you can create a `IasiL1cNativefile` object starting
from the path of a file:

```
iasi_file = IasiL1cNativeFile(file_path)
```

A `IasiL1cNativeFile` gives access to all the information stored in the
original file. For example, we can get the latitudes of the observations

```
latitudes = iasi_file.get_latitudes()
```

Other methods are: `get_longitudes`, `get_radiances`, `get_zenith_angles`,
`get_solar_zenith_angles`, `get_solar_azimuth_angles`, `get_avhrr_cloud_fractions`,
`get_land_fractions`, `get_date_day`, `get_date_msec`, `get_obs_times` and
`get_channels`.

If those methods are not enough, you can access to each record of the file with the
method `get_record(i)` where i is the index of the record (between 0 and the total
number of records of the file minus 1). You can check the total number of records
by reading the property `n_of_records` of the `IasiL1CNativeFile`.

If you want to access to a mdrs record, please call the method `read_mdrs` on the
file object in advance, othewise the content of the record will not be
interpreted (i.e., you will only receive a sequence of bytes).
