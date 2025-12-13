# CmdEntryObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code_block** | **str** | Code block extracted from prompt or response content | [optional] 
**verdict** | **str** | Detection service verdict such as \&quot;malicious\&quot; or \&quot;benign\&quot; | [optional] 

## Example

```python
from aisecurity.generated_openapi_client.models.cmd_entry_object import CmdEntryObject

# TODO update the JSON string below
json = "{}"
# create an instance of CmdEntryObject from a JSON string
cmd_entry_object_instance = CmdEntryObject.from_json(json)
# print the JSON string representation of the object
print(CmdEntryObject.to_json())

# convert the object into a dict
cmd_entry_object_dict = cmd_entry_object_instance.to_dict()
# create an instance of CmdEntryObject from a dict
cmd_entry_object_from_dict = CmdEntryObject.from_dict(cmd_entry_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


