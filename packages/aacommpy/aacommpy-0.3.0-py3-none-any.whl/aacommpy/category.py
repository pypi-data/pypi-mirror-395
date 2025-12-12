categories = [
    {"from": "AAComm", "name": "CommAPI", "enable": True},
    {"from": "AAComm", "name": "Shared", "enable": True},
    {"from": "AAComm", "name": "Services", "enable": True},
    {"from": "AAComm", "name": "CommAPIWrapper", "enable": True},
]
SharedCategories = [
    {"from": "AAComm.Shared", "name": "ChannelType", "enable": True},
    {"from": "AAComm.Shared", "name": "ConnectResult", "enable": True},
    {"from": "AAComm.Shared", "name": "ProductTypes", "enable": True},
]
Servicescategories = [
    {"from": "AAComm.Services", "name": "ConnectionData", "enable": True},
    {"from": "AAComm.Services", "name": "AllStatInterpreter", "enable": True},
    {"from": "AAComm.Services", "name": "ControllerMessagesContainer", "enable": True},
]
Extensionscategories = [
    {"from":"AAComm.Extensions", "name":"AACommDownloadFW","enable": True},
    {"from":"AAComm.Extensions", "name":"AACommDownloadUP","enable": True},
]
categories.extend(SharedCategories)
categories.extend(Servicescategories)
categories.extend(Extensionscategories)