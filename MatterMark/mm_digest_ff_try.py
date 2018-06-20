import json
from mattermark import mattermark

# #################################3
# Example usage of https://github.com/FoundryGroup/Mattermark
# ##################################


# Get Mattermark api configuration
# Use sandbox configuration for testing
def get_config():
    print("Reading configuration...")
    with open('sandbox_config.json') as config_file:
        try:
            config = json.load(config_file)
            print(json.dumps(config) + " \nsuccessful...")
            return config["mattermark"]
        except Exception as e:
            print("Error while reading config: {}".format(e))


api_key = get_config()["api_key"]
mm = mattermark(api_key)


# Search for the FoundryGroup
foundry_search = mm.investorSearch("Foundry Group")
print(foundry_search)
foundryID = foundry_search[0]["object_id"]

