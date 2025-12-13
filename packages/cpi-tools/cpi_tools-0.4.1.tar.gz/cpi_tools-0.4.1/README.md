# CPI Data Tools

A repository of commonly used tools across CPI

## Instructions

1. Install:

```
pip install cpi_tools
```

AWS Tools

```python
from cpi_tools import aws_tools

#S3 Bucket
bucket = 'YOUR_BUCKET'
#Path within S3
path = 'PATH_IN_BUCKET'
#S3 File name 
file_name = 'FILE_NAME'

#Read file from S3
df = aws_tools.read_from_s3(bucket, path, file_name)

#Write file to S3
aws_tools.write_to_s3(df, bucket, path, file_name)
```

