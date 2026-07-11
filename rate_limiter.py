import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Path

class RateLimiter:
    def __init__(self, port, username, password, host):
        self.r = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            username=username,
            password=password,
        )

    async def check_request(self, user_email) -> bool:
        current_user = await self.r.exists(user_email)
        if current_user:
            return True
        return False

    async def add_to_counter(self, user_email) -> dict[str, str]:
        the_user = None
        async with self.r.pipeline(transaction=True) as pipe:
            pipe.hincrby(user_email, "counter", 1)
            pipe.hgetall(user_email)
            the_user = await pipe.execute() #returns list of previous executed transac status
            print(the_user)

        return the_user[1]

    async def add_new_request(self, user_email) -> bool:
        new_user = {
            "counter": 1,
            "email": user_email,
        }

        try:
            add_new = await self.r.hsetex(name=user_email, mapping=new_user, ex=30)
            print("added")
        except Exception as err:
            # raise err
            print("did an error occur?")
            return False
        else:
            # print("new_user return value:", add_new)
            return True

    async def main(self, email:str = Path(...)) -> HTTPException | str:
            verify_user = await self.check_request(email)

            if verify_user:
                #       logic for checking if limit exceeded using pipe
                current_user = await self.add_to_counter(email)
                current_user_counter = int(current_user.get("counter"))

                if not current_user_counter or current_user_counter > 1:
                    # return print("access denied")
                    return HTTPException(status_code=429, detail="error, too many requests")


            await self.add_new_request(email)
            # print("executing requested page")
            return email


    async def close_redis(self):
        await self.r.aclose()

