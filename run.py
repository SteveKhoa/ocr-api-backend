"""Main server process 'uvicorn'
"""

import uvicorn
import os

environ = os.environ.get("ENVIRON")

if __name__ == "__main__":
    
    match environ:
        case "dev":
            uvicorn.run("app.main:app", reload=True)
        case "prod":
            print("Not implemented....sorry")
            print("Process stopped...")
            exit(0)
        case _:
            print("Undefined environment [{}]".format(environ))
            print("Process stopped...")
            exit(1)
