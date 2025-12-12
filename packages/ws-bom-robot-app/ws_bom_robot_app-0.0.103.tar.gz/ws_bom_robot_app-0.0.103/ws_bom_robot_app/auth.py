import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ws_bom_robot_app.config import config
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """_summary_
    Args:
        credentials (HTTPBasicCredentials, optional): _description_. Defaults to Depends(security).
    """
    def raise_error():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if credentials is None:
        raise_error()
    if not secrets.compare_digest(credentials.username, config.robot_user) or \
       not secrets.compare_digest(credentials.password, config.robot_password):
        raise_error()
    return True
