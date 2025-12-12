from enum import Enum


class EventType(Enum):
    REGISTRATION = "registration"
    BULK_OPERATION = "bulkoperation"
    CLOSE_PUBLICATION = "closepublication"
    CREATE = "create"
    DELETE = "delete"
    OPEN_PUBLICATION = "openpublication"
    PRINT = "print"
    PUT_TO_ARCHIVE = "puttoarchive"
    PUT_TO_RECYCLE_BIN = "puttorecyclebin"
    REPLACE_TOKEN = "replacetoken"
    RESTORE_FROM_ARCHIVE = "restorefromarchive"
    RESTORE_FROM_RECYCLE_BIN = "restorefromrecyclebin"
    SEND_EMAIL_FROM_ENTITY = "sendemailfromentity"
    UPDATE = "update"
