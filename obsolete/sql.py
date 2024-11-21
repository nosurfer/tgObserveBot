import sqlite3
import logging
import asyncio
import re
import os


async def stringFilter(string: str) -> str:
    string = re.sub(r"[\"\'\-*/#;&|(){}\\]", "", string)
    string = re.sub(r'--.*$', '', string)
    string = re.sub(r'/\*.*?\*/', '', string, flags=re.DOTALL)
    return string


class InteractionWithDB:
    """Easy way to interact with db"""

    def __init__(self) -> None:
        """Инициализация класса"""
        try:
            self.connection = sqlite3.connect(db_name, autocommit=True)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, __init__")


    async def insertUser(self, user_id: int, user_name: str) -> None:
        """
        Вставляет в users: user_id и fullname/tag (users)\n
        Ничего не возвращает
        """
        user_name = await stringFilter(user_name)
        sql_query = f"INSERT INTO users (user_id, user_name) VALUES ({user_id}, '{user_name}');"
        try:
            self.cursor.execute(sql_query)
            logging.info(f"{user_id} user has been added")
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, insertUser")
    

    async def insertGroup(self, group_id: int, group_name: str):
        '''
        Вставляет в groups: group_id и group_name (groups)\n
        Ничего не возвращает
        '''
        group_name = await stringFilter(group_name)
        sql_query = f"INSERT INTO groups (group_id, group_name) VALUES ({group_id}, '{group_name}');"
        try:
            self.cursor.execute(sql_query)
            logging.info(f"{group_id} {group_name} group has been added")
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, insertGroup")
    

    async def insertAdmin(self, group_id: int, *users_id: int) -> None:
        '''
        Сохраняет всех user_id как администраторов (group_admin)
        '''
        for user_id in users_id:
            sql_query = f"INSERT INTO group_admin (group_id, user_id) VALUES ({group_id}, '{user_id}');"
            try:
                self.cursor.execute(sql_query)
                logging.info(f"{group_id} users has been added like admins")
            except sqlite3.Error as error:
                logging.error(f"Sqlite error: {error}, insertAdmin")
    

    async def insertUserGroup(self, user_id: int, group_id: int) -> None:
        '''
        Привязывает к user_id соответствующий group_id (user_group)\n
        Ничего не возвращает
        '''
        sql_query = f"INSERT INTO user_group (user_id, group_id) VALUES ({user_id}, {group_id})"
        try:
            self.cursor.execute(sql_query)
            logging.info(f"{user_id} {group_id} group has been added to user")
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, insertUserGroup")
    

    async def selectUserGroup(self, user_id: int) -> list:
        '''
        Извлекает все group_id по user_id (user_group)
        Возвращет список всех group_id
        '''
        sql_query = f"SELECT group_id FROM user_group WHERE user_id = {user_id};"
        try:
            return self.cursor.execute(sql_query).fetchall()
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, selectUserGroup")
    

    async def selectGroup(self, group_id: int = None) -> list:
        '''
        Выдаёт group_name по group_id. (groups)
        Если параметр не указан - выдаёт все group_id и group_name.
        Возвращает список кортежей
        '''
        if group_id:
            sql_query = f"SELECT group_name FROM groups WHERE group_id = {group_id}"
        else:
            sql_query = "SELECT * FROM groups;"
        try:
            return self.cursor.execute(sql_query).fetchall()
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, selectGroup")


    async def deleteGroup(self, group_id: int, group_name: str) -> None:
        '''
        ДОРАБОТАТЬ
        '''
        sql_query = f"DELETE FROM groups WHERE group_id = {group_id};"
        try:
            self.cursor.execute(sql_query)
            logging.info(f"{group_id} {group_name} group has been deleted")
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, {group_id} {group_name} group has not been deleted")

    async def searchAdmin(self, group_id: int = None):
        '''
        Все user_id по group_id (group_admin)
        Все group_id и user_id
        '''
        if group_id:
            sql_query = f"SELECT user_id FROM group_admin WHERE group_id = {group_id};"
        else:
            sql_query = f"SELECT * FROM group_admin;"
        try:
            return self.cursor.execute(sql_query).fetchall()
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, searchAdmin")
        

    async def selectUser(self, user_id: int = None) -> list:
        '''
        Выдаёт user_name по user_id.
        Если параметр не указан - выдаёт user_id и user_name. (users)
        '''
        if user_id:
            sql_query = f"SELECT * FROM users WHERE user_id = {user_id}"
        else:
            sql_query = "SELECT * FROM users;"
        try:
            return self.cursor.execute(sql_query).fetchall()
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, selectUser")


    async def checkUserGroup(self, user_id: int, group_id: int) -> bool:
        '''
        Проверяет наличие группы в у пользователя (user_group)
        Возвращает bool
        '''
        sql_query = f"SELECT group_id FROM user_group WHERE user_id = {user_id};"
        try:
            if group_id in self.cursor.execute(sql_query).fetchall():
                logging.info(f"id = {group_id} for {user_id} has been searched")
                return True
            else:
                logging.info(f"id = {group_id} for {user_id} has not been searched")
                return False
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, checkGroup")


    async def checkUser(self, user_id: int) -> bool:
        """
        Проверяет, существует ли пользователь в системе. (users)
        """
        sql_query = f"SELECT * FROM users WHERE user_id = {user_id};"
        try:
            if self.cursor.execute(sql_query).fetchall():
                logging.info(f"id = {user_id} user has been searched")
                return True
            else:
                logging.info(f"id = {user_id} user has not been searched")
                return False
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, checkUser")


    async def checkGroup(self, group_id: int) -> bool:
        '''
        Проверяет наличие группы в системе. (groups)
        '''
        sql_query = f"SELECT group_id FROM groups WHERE group_id = {group_id};"
        try:
            if self.cursor.execute(sql_query).fetchall():
                logging.info(f"id = {group_id} group has been searched")
                return True
            else:
                logging.info(f"id = {group_id} group has not been searched")
                return False
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, searchGroup")


    async def clearTable(self, table_name) -> None:
        sql_query = f"DELETE FROM {table_name};"
        try:
            self.cursor.execute(sql_query)
        except sqlite3.Error as error:
            logging.error(f"Sqlite error: {error}, clearTable")