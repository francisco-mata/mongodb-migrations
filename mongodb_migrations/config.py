import argparse
import os
from configparser import ConfigParser
from enum import Enum
from typing import Dict, Any


class Execution(Enum):
    DOWNGRADE = 'execution_downgrade'
    MIGRATE = 'execution_migrate'


class Configuration(object):
    config_file = ''
    mongo_host = '127.0.0.1'
    mongo_port = 27017
    mongo_url = ''
    mongo_database = ''
    mongo_username = ''
    mongo_password = ''
    mongo_migrations_path = 'migrations'
    metastore = 'database_migrations'
    execution = Execution.MIGRATE
    to_datetime = None

    def __init__(self, config: Dict[str, Any]=None):
        os.system("env")
        dir = os.getcwd()
        print(f'Initial dir: {dir}')
        os.chdir(os.path.dirname(__file__))
        dir = os.getcwd()
        print(f'App dir: {dir}')

        print(f'Config file detected: {config}')
        print(f'ENV: {os.environ}')

        self.config_file = os.getenv(
            'MONGODB_MIGRATIONS_CONFIG',
            '/etc/migrations/config/config.ini'
        )

        if not config:
            print(f'Config file path: {self.config_file}')
            self._from_ini()
        else:
            self.mongo_host = config.get(
                'mongo_host', '127.0.0.1'
            )
            self.mongo_port = config.get(
                'mongo_port', 27017
            )
            self.mongo_url = config.get(
                'mongo_url', ''
            )
            self.mongo_database = config.get(
                'mongo_database', ''
            )
            self.mongo_username = config.get(
                'mongo_username', ''
            )
            self.mongo_password = config.get(
                'mongo_password', ''
            )
            self.mongo_migrations_path = config.get(
                'mongo_migrations_path', 'migrations'
            )
            self.metastore = config.get(
                'metastore', 'database_migrations'
            )
            self.execution = config.get(
                'execution', Execution.MIGRATE
            )
            self.to_datetime = config.get(
                'to_datetime', None
            )

            print(
                f'mongo_url: {self.mongo_url} \n'
                f'mongo_username: {self.mongo_username} \n'
                f'metastore: {self.metastore} \n'
                f'mongo_migrations_path: {self.mongo_migrations_path} \n'
                f'to_datetime: {self.to_datetime} \n'
            )

    def from_console(self):
        self.arg_parser = argparse.ArgumentParser(
            description="Mongodb migration parser"
        )
        self.arg_parser.add_argument(
            '--host', metavar='H', default=self.mongo_host,
            help="host of MongoDB"
        )
        self.arg_parser.add_argument(
            '--port', type=int, metavar='p', default=self.mongo_port,
            help="port of MongoDB"
        )
        self.arg_parser.add_argument(
            '--database', metavar='d',
            help='database of MongoDB', default=self.mongo_database)
        self.arg_parser.add_argument(
            '--username', metavar='U',
            help="username for auth database of MongoDB",
            default=self.mongo_username
        )
        self.arg_parser.add_argument(
            '--password', metavar='P',
            help="password for auth database of MongoDB",
            default=self.mongo_password
        )
        self.arg_parser.add_argument(
            '--url', metavar='u',
            help="Mongo Connection String URI", default=self.mongo_url)
        self.arg_parser.add_argument(
            '--migrations', default=self.mongo_migrations_path,
            help="directory of migration files")
        self.arg_parser.add_argument(
            '--downgrade', action='store_true',
            default=False, help='Downgrade instead of upgrade')
        self.arg_parser.add_argument(
            '--metastore', default=self.metastore,
            help='Where to store db migrations')
        self.arg_parser.add_argument(
            '--to_datetime', default=None,
            help=(
                "Upgrade/downgrade to reach the migration with the "
                "given datetime prefix"
            )
        )
        args = self.arg_parser.parse_args()

        self.mongo_url = args.url
        self.mongo_host = args.host
        self.mongo_port = args.port
        self.mongo_database = args.database
        self.mongo_username = args.username
        self.mongo_password = args.password
        self.mongo_migrations_path = args.migrations
        self.metastore = args.metastore
        self.to_datetime = args.to_datetime

        print('CLI Override flags')
        print(
            f'mongo_url: {self.mongo_url} \n'
            f'mongo_username: {self.mongo_username} \n'
            f'metastore: {self.metastore} \n'
            f'mongo_migrations_path: {self.mongo_migrations_path} \n'
            f'to_datetime: {self.to_datetime} \n'
        )

        if args.downgrade:
            self.execution = Execution.DOWNGRADE

    def _from_ini(self):
        self.ini_parser = ConfigParser(
            defaults={
                'host': self.mongo_host,
                'port': self.mongo_port,
                'migrations': self.mongo_migrations_path,
                'database': self.mongo_database,
                'username': self.mongo_username,
                'password': self.mongo_password,
                'url': self.mongo_url,
                'metastore': self.metastore
            }
        )

        try:
            fp = open(self.config_file)
            if bool(os.getenv('MONGODB_MIGRATIONS_DEBUG')) is True:
                print(f'Config file: {self.config_file}')
        except Exception:
            pass
        else:
            with fp:
                self.ini_parser.readfp(fp)

                print(f'Config file content: {self.ini_parser}')

                if not self.ini_parser.sections():
                    raise Exception(
                        f"Cannot find {self.config_file} or it doesn't "
                        f"have sections."
                    )

                self.mongo_url = self.ini_parser.get('mongo', 'url')
                self.mongo_host = self.ini_parser.get('mongo', 'host')
                self.mongo_port = self.ini_parser.getint('mongo', 'port')
                self.mongo_database = self.ini_parser.get('mongo', 'database')
                self.mongo_username = self.ini_parser.get('mongo', 'username')
                self.mongo_password = self.ini_parser.get('mongo', 'password')
                self.metastore = self.ini_parser.get('mongo', 'metastore')
                self.mongo_migrations_path = self.ini_parser.get(
                    'mongo', 'migrations'
                )

        print('File Config Override flags')
        print(
            f'mongo_url: {self.mongo_url} \n'
            f'mongo_username: {self.mongo_username} \n'
            f'metastore: {self.metastore} \n'
            f'mongo_migrations_path: {self.mongo_migrations_path} \n'
            f'to_datetime: {self.to_datetime} \n'
        )
