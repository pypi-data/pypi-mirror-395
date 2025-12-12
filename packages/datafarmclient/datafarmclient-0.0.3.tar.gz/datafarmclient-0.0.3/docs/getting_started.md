## Base class
The [DatafarmClient](reference.md/#datafarmclient.DatafarmClient) base class is where you want to start when you want to use this library.
You instantiate the base client by providing a valid api_url and then you login with a corresponding api_key.
```python
>>> from datafarmclient import DatafarmClient
>>> client = DatafarmClient(api_url=api_url)
>>> client.login(api_key=api_key)
True
```
After this you can explore the [properties](reference.md/#datafarmclient.DatafarmClient.locations) of the client that will tell you something about the database you are connected to, or you can start using the subclasses listed underneath.
## Entities
The entities subclass of the client is instantiated with an [EntityType](reference.md/#entitytype) to specify which entity you would like to interact with:
```python
>>> ts = client.entities("enTimeSeries")
>>> ts.metadata()
                                  Name    DataType  ...  NotNull  Encrypted
Idx                                                 ...                    
0                                   ID   ftInteger  ...     True      False
1                             EntityID   ftInteger  ...     True      False
2                              Touched  ftDateTime  ...    False      False
3                               IDName    ftString  ...     True      False
4                        IDDescription    ftString  ...    False      False
```
You can view the full list of entities specific functions in the [API Reference](reference.md/#datafarmclient.Entities)

## Timeseries
The timeseries subclass is created for easier tab-completion into timeseries specific operations.
```python
>>> client.timeseries.latest_values(time_series_id="test_ts_3")
                  DateTimeRef  Duration  Data  Quality  Confidence  ObjectSize
TsName                                                                        
test_ts_3 2020-01-02 11:00:00       NaN     1        4         NaN         NaN
```
You can view the full list of timeseries specific functions in the [API Reference](reference.md/#datafarmclient.TimeSeries)
## Variables
The variables subclass was created with python in mind. Keeping the dictionary getter and setter functionality you can easily use the client to access or alter the variables in the database.
```python
>>> client.variables["foo"] = "bar"
>>> client.variables["foo"]
"bar"
```
Through the variables subclass it is also possible to create new variable [categories](reference.md/#datafarmclient.Variables.create_category) and [types](reference.md/#datafarmclient.Variables.create_type)