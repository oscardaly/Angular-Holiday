# Angular-Holiday
An Angular webapp using a python API backend with MongoDB for COM661 coursework

alias mongod='brew services run mongodb-community'
alias mongod-status='brew services list'
alias mongod-stop='brew services stop mongodb-community'

To run the MongoDB Database, run - `mongod`
To stop the MongoDB Database, run - `mongod-stop`
To view the MongoDB interface, run - `mongosh`
To see the status of MongoDB Database, run - `mongod-status`

## To run this service
1. Run `mongod` from root
2. Run `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 /Users/oscardaly/Documents/Coding/Angular-Holiday/server/app.py`