[![Build Status](https://travis-ci.org/NSLS-II/simdb.svg)](https://travis-ci.org/NSLS-II/simdb)
[![Coverage Status](https://coveralls.io/repos/NSLS-II/simdb/badge.svg?branch=master)](https://coveralls.io/r/NSLS-II/simdb?branch=master)
[![Code Health](https://landscape.io/github/NSLS-II/simdb/master/landscape.svg?style=flat)](https://landscape.io/github/NSLS-II/simdb/master)
[![Join the chat at https://gitter.im/NSLS-II/simdb](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/NSLS-II/simdb?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# simdb
NSLS2 Beamlines simdb prototype implemented in MongoDB.

##Object Model
![simdb object model](https://github
.com/NSLS-IIsimdb/doc/simdb_object_model.png)

##What database technology is simdb using?
MongoDB.

##Where is this mongo database located?
Run this code snippet:
```python
import simdb
print(simdb.conf.connection_config)
```
And you will see this output.
```python
{'database': 'mds',
 'host': 'localhost',
 'port': 27017,
 'timezone': 'US/Eastern'}
```
Note that the values for `database`, `host`, `port`, `timezone` may be 
different.  
- `database` is the actual name of the mongo database
- `host` is the IP or DNS name of the server where the mongo database is 
  actually located
- `port` is the port that `mongoengine` and `pymongo` use to connect to the 
  `database` located at `host`
- `timezone` is the timezone of the database.

###Can I change where the mongo database is located at runtime?
Yes. For example:
```python
import simdb
new_database_name = 'one-database-to-rule-them-all'
new_host = '1.2.3.4'
simdb.conf.connection_config['database'] = new_database_name
simdb.conf.connection_config['host'] = new_host_name
```
After running this, simdb will be pointed at this new database for 
the duration of your python session. **Note that this change is not 
persistent between python sessions!**

##Description of the fields in each document
###BeamlineConfig
[Source] (https://github
.com/NSLS-II/simdb/blob/master/simdb/odm_templates.py#L17)

The beamline configuration is intentionally ambiguous and is generally left 
up to the user to decide.  It is intended to be 
a bucket for any and all information that is constant across multiple 
runs/scans, but can also be used to store run-specific information, if the 
user so chooses.

The following fields are guaranteed to be in each `BeamlineConfig` document.

- `uid`: A string unique identifier that may be provided to `simdb`. 
  If no uid is provided, `simdb` defaults to generating a `uuid4`.  
  **Note that this `uid` must be unique across all `BeamlineConfig` documents 
  that are stored in the database that simdb is currently pointing to.**
- `time`: The time that is provided to the `insert_beamline_config` 
  function in simdb, not when the document is saved into mongo.  In 
  practice, this difference is a few ms.
- `config_params`: A dictionary field that is otherwise free-form. This is 
  where all relevant information that you, the user, wish to store should go.

An example of the kind of information that might be good to store in the 
`BeamlineConfig` document would be the distance from the sample to the 
detector, various detector parameters (size of pixels in um), and perhaps a 
pointer to the most recent calibration scan.  Such a `BeamlineConfig` might 
look like this:

```
BeamlineConfig
==============
calibration_scan_uid      : 6e78b971-30bb-4f48-8621-1ab95c2ccf94    
config_params             :
detector_dist             : 100                                     
detector_dist_units       : cm                                      
detector_pixel_size       : (100, 100)                              
detector_pixel_size_units : um                                      
time                      : 1433449177.4622374                      
time_as_datetime          : 2015-06-04 16:19:37.462237              
uid                       : 4c2d54a4-be2f-4b65-a520-695566fe4aa2    
```
###RunStart
[Source] (https://github.com/NSLS-II/simdb/blob/master/simdb
/odm_templates.py#L33)

The RunStart document
