
from app.database import Base, engine, async_session
from litestar import Litestar, Controller, get, post, patch, delete
from litestar.exceptions import NotFoundException
from litestar.config.cors import CORSConfig
from sqlalchemy import select, delete as sql_delete
from app.models import Todo
from app.schemas import TodoSchema, UpdateTodoSchema

cors_config = CORSConfig(
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create database tables
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

class TodoController(Controller):
    path = "/todos"

    # Get all todos
    @get()
    async def get_todos(self) -> list[dict]:
        async with async_session() as session:
            result = await session.execute(
                select(Todo).order_by(Todo.id)
            )
            todos = result.scalars().all() #

            return [
                {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "priority": todo.priority,
                }
                for todo in todos
            ]

    # Add a new todo
    @post()
    async def add_todo(self, data: TodoSchema) -> dict:
        async with async_session() as session:
            new_todo = Todo(**data.model_dump())

            session.add(new_todo)
            await session.commit()
            await session.refresh(new_todo)

            return {
                "id": new_todo.id,
                "title": new_todo.title,
                "description": new_todo.description,
                "completed": new_todo.completed,
                "priority": new_todo.priority,
            }

    # Update a todo
    @patch("/{todo_id:int}")
    async def update_todo(
        self,
        todo_id: int,
        data: UpdateTodoSchema,
    ) -> dict:
        async with async_session() as session:
            todo = await session.get(Todo, todo_id)

            if todo is None:
                raise NotFoundException("Todo not found")

            update_data = data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(todo, key, value)

            await session.commit()
            await session.refresh(todo)

            return {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority,
            }

    # Delete todos by status
    @delete(status_code=200)
    async def delete_todos_by_status(
        self,
        status: str = "all",
    ) -> dict:
        async with async_session() as session:
            query = sql_delete(Todo)

            if status.lower() == "completed":
                query = query.where(Todo.completed.is_(True))

            elif status.lower() == "active":
                query = query.where(Todo.completed.is_(False))

            elif status.lower() != "all":
                return {"message": "Invalid status"}

            result = await session.execute(query)
            await session.commit()

            return {
                "message": f"Deleted {result.rowcount} todo(s) successfully"
            }

    # Delete one todo by ID
    @delete("/{todo_id:int}", status_code=200)
    async def delete_todo(self, todo_id: int) -> dict:
        async with async_session() as session:
            todo = await session.get(Todo, todo_id)

            if todo is None:
                raise NotFoundException("Todo not found")

            await session.delete(todo)
            await session.commit()

            return {"message": "Todo deleted successfully"}


cors_config = CORSConfig(
    allow_origins=["http://localhost:5173"]
)


app = Litestar(
    route_handlers=[TodoController],
    on_startup=[create_tables],
    cors_config=cors_config,
)
