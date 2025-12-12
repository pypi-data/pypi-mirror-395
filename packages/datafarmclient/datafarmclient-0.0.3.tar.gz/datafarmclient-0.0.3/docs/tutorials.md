## Create a new timeseries
The entities subclass of the client is instantiated with an [EntityType](reference.md/#entitytype) to specify which entity you would like to interact with:

```python
>>> client.entities("enTimeSeries").exists("test_ts")
False
```
If the entity doesn't exist we can then create it with
```
>>> client.entities("enTimeSeries").create(
        "test_ts",
        fields={
            "IDDescription": "test_ts_1"
        }
    )
"EntityID999"
```
The response is then the entityID of the newly created timeseries.