import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # response = await session.post(url='http://127.0.0.1:8080/hello/world?k1=v1&k2=v2',
        #                               json={'json_key': 'json_value'},
        #                               headers={'token': '123456789'},
        #                               params={'k3': 'v3', 'k4': 'v4'}
        #                               )

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

        print('patch')
        response = await session.patch(url='http://127.0.0.1:8080/users/1',
                                      json={'name': 'user_2'})

        print(response.status)
        json_data = await response.json()
        print(json_data)

        print('get')
        response = await session.get(url='http://127.0.0.1:8080/users/1')

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
