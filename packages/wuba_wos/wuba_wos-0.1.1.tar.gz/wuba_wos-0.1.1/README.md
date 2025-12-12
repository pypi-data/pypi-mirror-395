## WOS

A Python client for the WOS (WuBa Object Storage) REST API.


### Usage
```python
from wos import WOS
# bucket: 存储桶名称; app_id: 应用ID; secret_id: 密钥ID
wos = WOS(bucket="your-bucket-name", app_id="your-app-id", secret_id="your-secret-id")
# 上传文件
result = wos.upload(filename = "test.txt", file_path = "test.txt")
# 删除文件
wos.delete(filename = "test.txt")
```
