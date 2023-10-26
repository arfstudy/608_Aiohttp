import json

from aiohttp import web
from bcrypt import checkpw, hashpw, gensalt
from sqlalchemy.exc import IntegrityError

from models import Base, engine, Session, User

app = web.Application


def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password


def check_password(password: str, db_password_hash: str):
    password = password.encode()
    db_password_hash = db_password_hash.encode()
    return checkpw(password, db_password_hash)


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({'error': 'User not found'}),
                               content_type='application/json')
    return user

class UserView(web.View):

    @property
    def session(self):
        return self.request['session']

    @property
    def user_id(self):
        return int(self.request.match_info['user_id'])

    async def get(self):
        user = await get_user(self.user_id, self.session)
        return web.json_response({
            'Получен id': user.id,
            'name': user.name,
            'creation_time': int(user.creation_time.timestamp())
        })

    async def post(self):
        json_data = await self.request.json()
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({'error': 'User already exists'}),
                                   content_type='application/json')
        return web.json_response({
            'Создан id': user.id
        })  # Поле 'creation_time' вернуть сразу не можем, т.к. оно динамически формируемое. Надо перезагрузить объект.

    async def patch(self):
        json_data = await self.request.json()
        if json_data['password'] is not None:
            json_data['password'] = hash_password(json_data['password'])
        user = await get_user(self.user_id, self.session)
        for field, value in json_data.items():
            setattr(user, field, value)
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({'error': 'User already exists'}),
                                   content_type='application/json')
        return web.json_response({'Изменён id': user.id})

    async def delete(self):
        user = await get_user(self.user_id, self.session)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({'Удалён id': user.id})


async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    print('SHUT DOWN')
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

app.add_routes([web.get('/users/{user_id:\d+}', UserView),
                web.post('/users/', UserView),
                web.patch('/users/{user_id:\d+}', UserView),
                web.delete('/users/{user_id:\d+}', UserView)])


if __name__ == '__main__':
    web.run_app(app)
