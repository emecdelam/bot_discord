import json
from typing import Dict,Any,List
from logging_system import log__,Level
from discord import User


class Assignment:
    def __init__(self,name: str,date: str,users:List[User] = None):
        if users is None:
            self.users = []
        self.name: str = name
        self.date: str = date
        self.users = users
        self.user_dic = {}
        for user in self.users:
            self.user_dic[user.id]="False"

    def add(self,user: User) -> None:
        if user in self.users:
            return
        self.users.append(user)

    async def save(self) -> None:
        if not await self.__name_already_exist(self.name):
            await self.__add_data(self.name,{"date":self.date,"users":self.user_dic})

    async def __read_data(self) -> Dict[str,Any]:
        try:
            with open("ex_reminder\\ongoing_assignments.json","r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            await log__(f"Couln't read data\n{e}",Level.ERROR)

    async def __add_data(self,new_name: str,new_data: Dict[str,Any]) -> None:
        try:
            data = await self.__read_data()
            if await self.__name_already_exist(new_name):
                await log__(f"Tried to add two times same data, might override-> use edit",Level.WARNING)
                return
            data[new_name] = new_data
            with open("ex_reminder\\ongoing_assignments.json","w") as file:
                json.dump(data,file,indent = 4)
        except Exception as e:
            await log__(f"Couldn't write new assignment\n{e}",Level.ERROR)
    async def __edit_data(self,name:str,new_data:Dict[str,Any]) -> None:
        try:
            data = await self.__read_data()
            if not await self.__name_already_exist(name):
                await log__(f"Tried to add the data when editing it might remove data use -> add",Level.WARNING)
                return
            data[name] = new_data
            with open("ex_reminder\\ongoing_assignments.json","w") as file:
                json.dump(data,file,indent = 4)
        except Exception as e:
            await log__(f"Couldn't write new assignment\n{e}",Level.ERROR)

    async def __name_already_exist(self,name: str) -> bool:
        if name in await self.__read_data():
            return True
        return False
    def __str__(self) -> str:
        return f"name : {self.name}, date : {self.date}, users : {[user.name for user in self.users]}"