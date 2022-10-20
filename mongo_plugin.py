from main import pe


@pe.hookimpl
def store_db(data):
    print('*'*40)
    print('MongoDB Data')
    print(data)
    print('*'*40)
