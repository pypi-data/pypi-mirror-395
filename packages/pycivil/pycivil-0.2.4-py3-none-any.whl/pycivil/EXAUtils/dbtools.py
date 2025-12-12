import pprint
from typing import Any, Dict, List, Union, Literal

import pymongo

# importing ObjectId from bson library
from bson.objectid import ObjectId
from dotenv.variables import Literal
from pydantic_settings import BaseSettings
from pymongo.database import Collection, Database

from pycivil.EXAUtils.logging import log


class DatabaseSettings(BaseSettings):
    """Database settings fetched via environment variables."""

    host: str = "localhost"
    port: int = 27017
    username: Union[str, None] = None
    password: Union[str, None] = None

    class Config:
        """set the prefix for the env vars."""

        env_prefix = "DB_"


class DbManager:
    def __init__(self):
        self.__config = DatabaseSettings()
        # self.__host: str = 'localhost:27017'
        # self.__host: str = '127.0.0.1:27017'
        self.__timeOut: int = 6000
        self.__client: Union[pymongo.MongoClient[Dict[str, Any]], None] = None
        self.__db: Union[Database[dict[str, Any]], None] = None
        self.__cl: Union[Collection[dict[str, Any]], None] = None
        self.__ll: Literal[0, 1, 2, 3] = 3

    def __del__(self):
        if self.__client is None:
            return
        try:
            self.__client.close()
            log("INF", "Closed connection to server", self.__ll)
        except Exception:
            log("ERR", "I cannot close connection to server !!!", self.__ll)

    def connect(self) -> bool:
        if self.__client is not None:
            return True
        host = self.__config.host
        port = self.__config.port
        try:
            self.__client = pymongo.MongoClient(
                host=host,
                port=port,
                username=self.__config.username,
                password=self.__config.password,
                serverSelectionTimeoutMS=self.__timeOut,
                uuidRepresentation="standard",
            )
            log("INF", "Connection to server created, checking...", self.__ll)
            self.__client.server_info()
        except Exception as ex:
            log("ERR", f"Can't connect to database!!! {ex}", self.__ll)
            log(
                "ERR",
                f"host: {host}:{port} - timeout: {self.__timeOut}",
                self.__ll,
            )
            return False
        return True

    def newDb(self, dbName: str) -> bool:
        if self.__client is None:
            log("ERR", "Client not available !!!", self.__ll)
            return False
        if dbName in self.__client.list_database_names():
            log("ERR", f"dbName <{dbName}> yet unavailable !!!", self.__ll)
            return False
        self.__db = self.__client[dbName]
        self.__cl = self.__db["fuck_collection"]
        self.__cl.insert_one({})
        log(
            "INF",
            "after insert newDb databases: {}".format(
                self.__client.list_database_names()
            ),
            self.__ll,
        )
        return True

    def existsDb(self, dbName: str) -> bool:
        if self.__client is None:
            log("ERR", "Client not available !!!", self.__ll)
            return False
        return dbName in self.__client.list_database_names()

    def setCurrentDb(self, dbName: str) -> bool:
        if self.__client is not None:
            if dbName in self.__client.list_database_names():
                self.__db = self.__client[dbName]
                log("INF", f"dbName <{dbName}> make current", self.__ll)
                return True
            else:
                log("ERR", f"dbName <{dbName}> not available !!!", self.__ll)
                return False
        else:
            log("ERR", "Client not available !!!", self.__ll)
            return False

    def dropDb(self, dbName: str) -> bool:
        if self.__client is not None:
            if dbName in self.__client.list_database_names():
                self.__client.drop_database(dbName)
                log("INF", f"dbName <{dbName}> removed", self.__ll)
                log(
                    "INF",
                    f"databases: {self.__client.list_database_names()}",
                    self.__ll,
                )
                return True
            else:
                log("ERR", f"dbName <{dbName}> not available !!!", self.__ll)
                return False
        else:
            log("ERR", "Client not available !!!", self.__ll)
            return False

    def newCollection(self, collectionName: str) -> bool:
        if self.__db is not None:
            if collectionName not in self.__db.list_collection_names():
                self.__cl = self.__db[collectionName]
                self.__cl.insert_one({})
                log(
                    "INF",
                    f"collections: {self.__db.list_collection_names()}",
                    self.__ll,
                )
                return True
            else:
                log(
                    "ERR",
                    f"collection <{collectionName}> yet unavailable",
                    self.__ll,
                )
                return False
        else:
            log("ERR", "Db not available !!!", self.__ll)
            return False

    def setCurrentCollection(self, collectionName: str) -> bool:
        if self.__db is not None:
            if collectionName in self.__db.list_collection_names():
                self.__cl = self.__db[collectionName]
                log(
                    "INF",
                    f"collection <{collectionName}> make current",
                    self.__ll,
                )
                return True
            else:
                log(
                    "ERR",
                    f"collection <{collectionName}> not available !!!",
                    self.__ll,
                )
                return False
        else:
            log("ERR", "Client not available !!!", self.__ll)
            return False

    def newDocument(self, doc: Dict[str, Any]) -> str:
        if self.__cl is not None:
            id = self.__cl.insert_one(doc).inserted_id
            log("INF", f"doc added with id <{str(id)}>", self.__ll)
            return str(id)
        else:
            log("ERR", "None current collection available !!!", self.__ll)
            return ""

    def findOne(self, query: Dict[str, Any]) -> str:
        if self.__cl is not None:
            doc = self.__cl.find_one(query)
            if isinstance(doc, dict):
                log("INF", "doc found with id <{}>".format(str(doc["_id"])), self.__ll)
                return str(doc["_id"])
            else:
                log("ERR", "doc not found !!!", self.__ll)
                return ""
        else:
            log("ERR", "None current collection available !!!", self.__ll)
            return ""

    def getAllDocsFromCollection(self) -> Union[List[Dict], None]:
        if self.__cl is not None:
            return list(self.__cl.find())
        else:
            log("ERR", "None current collection available !!!", self.__ll)
            return None

    def replaceOne(self, query: Dict[str, Any], doc: Dict[str, Any]) -> bool:
        if self.__cl is None:
            log("ERR", "No current collection available !!!", self.__ll)
            return False
        mc = self.__cl.replace_one(query, doc).matched_count
        if mc == 0:
            log("INF", f"no document updated with query <{query}>", self.__ll)
            return False
        log("INF", "Doc updated", self.__ll)
        return True

    def findById(self, id: str) -> Dict[str, Any]:
        try:
            objectId = ObjectId(id)
        except Exception:
            log(
                "ERR",
                f"id <{id}> not compliant with possibilities given by QObject class!!!",
                self.__ll,
            )
            return {}

        if self.__cl is None:
            log("ERR", "No current collection available !!!", self.__ll)
            return {}
        doc = self.__cl.find_one({"_id": objectId})
        if isinstance(doc, dict):
            log("INF", "doc found by id <{}>".format(str(doc["_id"])), self.__ll)
            return doc
        log("ERR", "doc not found !!!", self.__ll)
        return {}

    def deleteById(self, id: str) -> int:
        try:
            objectId = ObjectId(id)
        except Exception:
            log(
                "ERR",
                f"id <{id}> not compliant with possibilities given by QObject class!!!",
                self.__ll,
            )
            return 0

        if self.__cl is None:
            log("ERR", "No current collection available !!!", self.__ll)
            return 0
        count = self.__cl.delete_one({"_id": objectId}).deleted_count
        if count > 0:
            log("INF", f"doc removed by id <{id}>", self.__ll)
            return count
        log("ERR", f"doc did not removed by id <{id}>", self.__ll)
        return 0

    def __str__(self) -> str:
        lines = []
        if self.__client is not None:
            lines.append(f"Database names: {self.__client.list_database_names()}")
        if self.__db is not None:
            lines.append(f"Collection names: {self.__db.list_collection_names()}")
        if self.__cl is not None:
            lines.append(f"Documents nb: {self.__cl.count()}")
        return "\n".join(lines)

    def printCollection(self) -> None:
        if self.__cl is None:
            log("ERR", "None current collection available !!!", self.__ll)
            return
        cursor = self.__cl.find({})
        for document in cursor:
            pprint.pprint(document, indent=4)
