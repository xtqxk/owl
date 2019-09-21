USAGE
-----
## Tornado
### step 1:
Type the template class
```python
class DemoCfgOptions(object):
    __base_key__ = "myroot"
    '''
     # the default value is just type template,
     # if key in consul k/v, the value will override by consul
    '''
    api_url = "h"
    api_port = 0
    admin_emails = []
    uname=""
```
### step 2:
patch the instance of config template, like this:
```python
loop = IOLoop.instance()
xcfg = t_options.DynamicPatch(loop,op)
```
if you what to listen key change event callback.
```python
xcfg.add_change_callback("api_url","uname", callback_handler=on_callback)
xcfg.add_change_callback("api_port", callback_handler=on_other_callback)
```

### step 3:
start loop use xcfg
```python
xcfg.start()
```
or start the tornado ioloop directly.
```python
loop.start()
```
