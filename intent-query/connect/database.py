import psycopg2
import snowflake.connector
import os.path
import json


class Database:
    def __init__(self, type):
        self.__dbtype = type.lower()
        self.__creds = self._get_credentials()

    @property
    def dbtype(self):
        return self.__dbtype

    def _get_credentials(self):
        creds = None
        this_path = os.path.dirname(os.path.abspath(__file__))
        json_path = this_path + '/credentials.json'

        # credentials.json stores the user's information including username, password,
        # database, port, etc. users will be prompted to create one if one does not exist
        if os.path.exists(json_path):
            try:
                creds = self._read_creds_file(json_path, self.dbtype)
            except KeyError:
                # get user input for their credentials depending on the dbtype
                if not creds:
                    creds_file = self._read_creds_file(json_path)
                    creds = self._get_user_input_creds()
                    creds_file[self.dbtype] = creds
                    self._write_creds_file(creds_file)
        # return credentials as python dictionary
        return creds

    @property
    def credentials(self):
        return self.__creds

    def _get_user_input_creds(self):
        params_switch = {
            'snowflake': ('user', 'password', 'account', 'database', 'schema')
        }
        params = params_switch.get(self.dbtype, 'Invalid Database Type')

        print("Please enter the following details:", '\n')
        responses = {param: input(str(param) + ": ")
                     for param in params}
        return responses

    def _read_creds_file(self, path, dbtype=None):
        with open(path) as file:
            j_file = json.load(file)[dbtype] if dbtype else json.load(file)
        return j_file

    def _write_creds_file(self, creds_dic):
        this_path = os.path.dirname(os.path.abspath(__file__))
        json_path = this_path + '/credentials.json'

        with open(json_path, 'w') as write_file:
            json.dump(creds_dic, write_file, indent=2)
        pass


if __name__ == '__main__':
    db = Database(type='snowflake')
    print(db.credentials)
