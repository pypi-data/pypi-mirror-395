from .singleton import Singleton


class ProgressionTypes(metaclass=Singleton):
    __progression_types = {
        "default": [
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 10000},
                "mutatorId": "400274122",
            }
        ],
        "portal-standard": [
            {
                "name": "MasteryLevelCap",
                "category": "Persistence",
                "kind": {"intValue": 1},
                "mutatorId": "2587263936",
            },
            {
                "name": "AwardFilter",
                "category": "Persistence",
                "kind": {
                    "boolSparse": {
                        "sparseValues": [
                            {"index": 0, "value": None},
                            {"index": 1, "value": True},
                            {"index": 2, "value": None},
                            {"index": 3, "value": None},
                            {"index": 4, "value": None},
                            {"index": 5, "value": None},
                            {"index": 6, "value": None},
                            {"index": 7, "value": None},
                            {"index": 8, "value": None},
                            {"index": 9, "value": None},
                            {"index": 10, "value": None},
                            {"index": 11, "value": True},
                        ],
                        "defaultValue": True,
                    }
                },
                "mutatorId": "3878594831",
            },
            {
                "name": "PersistStats",
                "category": "Persistence",
                "kind": {"boolValue": False},
                "mutatorId": "877869937",
            },
            {
                "name": "ProgressionModeUIType",
                "category": "Persistence",
                "kind": {"intValue": 2},
                "mutatorId": "1058629035",
            },
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 300},
                "mutatorId": "400274122",
            },
        ],
        "portal-featured": [
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 10000},
                "mutatorId": "400274122",
            }
        ],
        "solo-coop": [
            {
                "name": "MasteryLevelCap",
                "category": "Persistence",
                "kind": {"intValue": 12},
                "mutatorId": "2587263936",
            },
            {
                "name": "AwardFilter",
                "category": "Persistence",
                "kind": {
                    "boolSparse": {
                        "sparseValues": [
                            {"index": 0, "value": None},
                            {"index": 1, "value": True},
                            {"index": 2, "value": True},
                            {"index": 3, "value": None},
                            {"index": 4, "value": True},
                            {"index": 5, "value": True},
                            {"index": 6, "value": None},
                            {"index": 7, "value": None},
                            {"index": 8, "value": None},
                            {"index": 9, "value": True},
                            {"index": 10, "value": True},
                            {"index": 11, "value": True},
                            {"index": 12, "value": None},
                        ],
                        "defaultValue": True,
                    }
                },
                "mutatorId": "3878594831",
            },
            {
                "name": "PersistStats",
                "category": "Persistence",
                "kind": {"boolValue": False},
                "mutatorId": "877869937",
            },
            {
                "name": "ProgressionModeUIType",
                "category": "Persistence",
                "kind": {"intValue": 1},
                "mutatorId": "1058629035",
            },
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 100},
                "mutatorId": "400274122",
            },
        ],
        "portal-default": [
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 10000},
                "mutatorId": "400274122",
            }
        ],
        "portal-unranked": [
            {
                "name": "AwardFilter",
                "category": "Persistence",
                "kind": {
                    "boolSparse": {
                        "sparseValues": [
                            {"index": 0, "value": None},
                            {"index": 1, "value": True},
                            {"index": 2, "value": None},
                            {"index": 3, "value": None},
                            {"index": 4, "value": None},
                            {"index": 5, "value": None},
                            {"index": 6, "value": None},
                            {"index": 7, "value": None},
                            {"index": 8, "value": None},
                            {"index": 9, "value": None},
                            {"index": 10, "value": None},
                            {"index": 11, "value": True},
                            {"index": 12, "value": None},
                            {"index": 13, "value": None},
                        ],
                        "defaultValue": True,
                    }
                },
                "mutatorId": "3878594831",
            },
            {
                "name": "MasteryLevelCap",
                "category": "Persistence",
                "kind": {"intValue": 1},
                "mutatorId": "2587263936",
            },
            {
                "name": "PersistStats",
                "category": "Persistence",
                "kind": {"boolValue": False},
                "mutatorId": "877869937",
            },
            {
                "name": "ProgressionModeUIType",
                "category": "Persistence",
                "kind": {"intValue": 2},
                "mutatorId": "1058629035",
            },
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 300},
                "mutatorId": "400274122",
            },
        ],
        "portal-spotlight": [
            {
                "name": "XpCapValue",
                "category": "Persistence",
                "kind": {"intValue": 10000},
                "mutatorId": "400274122",
            }
        ],
    }

    async def updateProgression(self, progression_types: dict):
        self.__progression_types = progression_types

    async def get(self):
        return self.__progression_types


async def getProgressionType(item: str):
    progression_types = ProgressionTypes()
    progression_types_list = await progression_types.get()
    return progression_types_list.get(item, {})
