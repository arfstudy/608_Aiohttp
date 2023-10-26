import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        print('post')
        response = await session.post(url='http://127.0.0.1:8080/users',
                                      json={'name': 'user_1', 'password': '1234'})

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('get')
        response = await session.get(url='http://127.0.0.1:8080/users/1')

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('post')
        response = await session.post(url='http://127.0.0.1:8080/users',
                                      json={'name': 'user_2', 'password': '4321'})

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('get')
        response = await session.get(url='http://127.0.0.1:8080/users/2')

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('patch')
        response = await session.patch(url='http://127.0.0.1:8080/users/2',
                                      json={'name': 'new_user_2'})

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('get')
        response = await session.get(url='http://127.0.0.1:8080/users/2')

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('delete')
        response = await session.delete(url='http://127.0.0.1:8080/users/1',
                                      json={'name': 'user_2'})

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('get')
        response = await session.get(url='http://127.0.0.1:8080/users/1')

        print(response.status)
        json_data = await response.json()
        print(json_data)


asyncio.run(main())
