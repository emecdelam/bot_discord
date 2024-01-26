from typing import Dict

import pickle


class Debt:
    def __init__(self,user_id: int):
        self.paid: int = 0
        self.debt: int = 0
        self.user_id: int = user_id

    async def add_debt(self,amount: float) -> None:
        self.debt += amount

    async def remove_debt(self,amount: float) -> None:
        self.paid += amount

    async def due(self) -> float:
        return self.debt - self.paid

    async def update_debt(self) -> None:
        messages = pickle.load(open("db\\messages.p","rb"))
        score = {}

        for message in messages.keys():
            if self.user_id not in messages[message].keys():
                continue

            if messages[message][self.user_id]:
                if self.user_id in score:
                    score[self.user_id] += 5
                else:
                    score[self.user_id] = 5
        if self.user_id in score.keys():
            self.debt = score[self.user_id]

    async def get_debt(self) -> float:
        await self.update_debt()
        return self.debt


class Debts:
    def __init__(self):
        self.debts: Dict[int,Debt] = {}

    def add_debt(self,debt: Debt) -> None:
        self.debts[debt.user_id] = debt

    def get_debt(self,id: int) -> Debt:
        if id in self.debts.keys():
            return self.debts[id]
        return Debt(id)


async def save_debts(debts: Debts) -> None:
    pickle.dump(debts,open("db\\debts.p","wb"))


async def read_debts() -> Debts:
    return pickle.load(open("db\\debts.p","wb"))
