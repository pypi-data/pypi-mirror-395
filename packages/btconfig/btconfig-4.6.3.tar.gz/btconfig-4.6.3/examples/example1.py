from btconfig import Config
# Initialize App Config
config = Config(config_file_uri='myconfig1.yaml', templatized=True).read()
value = config.get('section1.key4')
print(value)
print(config)