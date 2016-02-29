email = 'test@test.com'
password = 'test123'

modules = [
    'sample'
]

web = True
web_opts = {
    'listen_host': 'localhost',
    'listen_port': 8080
}
manhole = True
manhole_opts = {
    'listen_port': 9001,
}

storage = 'shelve'
storage_opts = {
    'shelve_data_path': './shelve'
}
