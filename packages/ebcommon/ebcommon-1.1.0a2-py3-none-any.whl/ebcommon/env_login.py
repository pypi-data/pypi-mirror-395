import os
import requests
import logging
from ebcommon.models_common   import UserCred, MessageLogin, MessageException

def env_login(baseurl: str = "https://ebuffer.aqmo.org/api/v1", user: str = "admin") -> MessageLogin:
    """
    """
    m_baseurl = os.getenv('EB_URL', baseurl)
    m_user = os.getenv('EB_USER', user)
    m_password = os.getenv('EB_PASS', user)
    u_maintainer = UserCred(username=m_user, password=m_password)
    token = os.getenv('EB_TOKEN', r'')

    try:
        if not token:
            logging.debug(f"[Login] using login/password: {m_user}/{m_password}")
            response = requests.post(f"{m_baseurl}/auth/login", u_maintainer.model_dump_json())
            uatoken = MessageLogin.castResponse(response)
            if uatoken.error_level != 0: raise RuntimeError(f"[Loging] error: {uatoken}")
            logging.info(f"[Login] Connected: {uatoken}")
        else:
            uatoken = MessageLogin(token)
            logging.info(f"[Login] using token: {uatoken}")
        return uatoken
    except (ConnectionError, MessageException) as m:
        raise RuntimeError("[Login] connexion error.") from m
