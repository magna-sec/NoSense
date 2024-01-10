import Utils.Database
import Utils.Login as Login

from termcolor import cprint

class Target():
    def __init__(self) -> None:
        """Initialises the object.

        Args:
          None.
        """
        self.dbConn = Utils.Database()
        self.DEBUG = False

    def get_targets(self) -> tuple:
          """
          """
          targets = []
          # Used for the menu
          id = self.dbConn.get_all_rows("id", "firewalls")
          name = self.dbConn.get_all_rows("name", "firewalls")
          ip = self.dbConn.get_all_rows("ip", "firewalls")

          for i in range(len(name)):
              targets.append(f"{id[i]}: {name[i]}:{ip[i]}")
          targetsLen = len(name)
          targets.append(f"99: All Targets")
        
          return targets

    def get_shells(self, shellType: str) -> tuple:
          """
          """
          shells = []
          # Used for the menu
          id = self.dbConn.get_all_rows("id", shellType)
          names = self.dbConn.get_all_rows("name", shellType)
          url = self.dbConn.get_all_rows("url", shellType)
          paths = self.dbConn.get_all_rows("path", shellType)
          level = self.dbConn.get_all_rows("level", shellType)

          for i in range(len(names)):
              shells.append(f"{id[i]}: {names[i]}: {url[i]}{paths[i]} - {level[i]}")

          return shells
    
    def get_keys(self) -> tuple:
          """
          """
          keys = []
          # Used for the menu
          id = self.dbConn.get_all_rows("id", "sshkeys")
          names = self.dbConn.get_all_rows("name", "sshkeys")
          ip = self.dbConn.get_all_rows("ip", "sshkeys")
          user = self.dbConn.get_all_rows("url", "sshkeys")
          keyfile = self.dbConn.get_all_rows("keyfile", "sshkeys")

          for i in range(len(names)):
              keys.append(f"{id[i]}: {names[i]}: {ip[i]}{user[i]}")
        
          print(keys)
          return keys
    
    def get_users(self, target, ip) -> tuple:
          """
          """
          listOfUsers = []
          # Used for the menu
          id = self.dbConn.get_all_rows_where("id", "sshkeys", "ip", ip)
          user = self.dbConn.get_all_rows_where("user", "sshkeys", "ip", ip)

          for i in range(len(user)):
              listOfUsers.append(f"{id[i]}: {user[i]}")
        
          return listOfUsers
    
    def get_user_from_id(self, id:str) -> str:
          """
          """
          user = self.dbConn.get_all_rows_where("user", "sshkeys", "id", id)[0]
          if(self.DEBUG): print(f"[+] GetUserFromId:user: {user}")
          return user
    
    def get_session(self, id:str, login:bool=True):
         """
         """
         name = self.dbConn.get_all_rows_where("name", "firewalls", "id", id)[0]
         url = self.dbConn.get_all_rows_where("url", "firewalls", "id", id)[0]
         username = self.dbConn.get_all_rows_where("username", "firewalls", "id", id)[0]
         password = self.dbConn.get_all_rows_where("password", "firewalls", "id", id)[0]

         return Login.Login(name, url, username, password, login)