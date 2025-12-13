from aldera.sms.backends import aws, locmem

backend_classes = {
    'aws': aws.SmsBackend,
    'locmem': locmem.SmsBackend,
}

try:
    from aldera.sms.backends import async_aws
except ModuleNotFoundError:
    pass
else:
    backend_classes['async_aws'] = async_aws.AsyncSmsBackend
