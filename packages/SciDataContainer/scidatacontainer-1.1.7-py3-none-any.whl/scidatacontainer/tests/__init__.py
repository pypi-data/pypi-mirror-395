import scidatacontainer

import uuid


def get_test_container():
    parameter = {
                 "acquisition": {
                                 "acquisitionMode": "SingleFrame",
                                 "exposureAuto": "Off",
                                 "exposureMode": "Timed",
                                 "exposureTime": 19605.0,
                                 "gain": 0.0,
                                 "gainAuto": "Off",
                                 "gainMode": "Default",
                                 "gainSelector": "AnalogAll"
                                 },
                 "device": {
                            "family": "mvBlueFOX3",
                            "id": 0,
                            "product": "mvBlueFOX3-2032aG",
                            "serial": "FF008343"
                            },
                 "format": {
                            "height": 1544,
                            "offsetX": 0,
                            "offsetY": 0,
                            "width": 2064
                            }
                 }
    data = [[i for i in range(256)] for j in range(128)]
    name = "John Doe"
    email = "john@example.com"
    org = "Example ORG"

    timestamp = scidatacontainer.timestamp()
    items = {
             "content.json": {
                 "uuid": "00000000-0000-0000-0000-000000000000",
                 "replaces": "00000000-0000-0000-0000-000000000001",
                 "containerType": {"name": "TestType",
                                   "id": "TestID",
                                   "version": "0.1"
                                   },
                 "usedSoftware": [
                                  {"name": "testSoftware1",
                                   "version": "0.2",
                                   },
                                  {"name": "testSoftware2",
                                   "version": "0.3",
                                   "id": "TestID2",
                                   "idType": "URL",
                                   },
                                  ],
                 "complete": True,
                 "static": False,
                 "created": timestamp,
                 "storageTime": timestamp,
                 },
             "meta.json": {
                 "author": name,
                 "email": email,
                 "organization": org,
                 "comment": "Example comment",
                 "title": "This is a sample image dataset",
                 "keywords": ["keyword1", "keyword2", "keyword3"],
                 "description": "Example description",
                 "doi": "https://example.com/" + str(uuid.uuid4()),
                 "license": "MIT",
                 "timestamp": timestamp,
                 },
             "meas/image.tsv": data,
             "data/parameter.json": parameter,
             }
    return scidatacontainer.Container(items=items)
