import json


# Get Mattermark api configuration
# Use sandbox configuration for testing
def get_config():
    with open('config.json') as config_file:
        try:
            config = json.load(config_file)
            print(json.dumps(config) + " \nsuccessful...")
            return config["mattermark"]
        except Exception as e:
            print("Error while reading config: {}".format(e))


def get_api_key(config):
    return config["api_key"]


def get_uri(config):
    return config["base_uri"]


# Gmail credentials for daily mails
def get_mail_credentials():
    with open('config.json') as config_file:
        try:
            config = json.load(config_file)
            return config["mailing"]
        except Exception as e:
            print("Error while reading config: {}".format(e))


def get_mail_address(config):
    return config["address"]


def get_mail_pass(config):
    return config["password"]
