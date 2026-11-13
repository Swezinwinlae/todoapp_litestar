
from app.database import Base, engine, async_session
from litestar import Litestar, get, post, patch, delete
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


# Get all todos
@get("/todos")
async def get_todos() -> list[dict]:
    async with async_session() as session:
        result = await session.execute(select(Todo).order_by(Todo.id))
        todos = result.scalars().all()

        return [
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority
            }
            for todo in todos
        ]


# Create a new todo
@post("/todos")
async def add_todo(data: TodoSchema) -> dict:
    async with async_session() as session:
        new_todo = Todo(
            title=data.title,
            description=data.description,
            completed=data.completed,
            priority=data.priority
        )

        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)

        return {
            "id": new_todo.id,
            "title": new_todo.title,
            "description": new_todo.description,
            "completed": new_todo.completed,
            "priority": new_todo.priority
        }

# Update one todo
@patch("/todos/{todo_id:int}")
async def update_todo(todo_id: int, data: UpdateTodoSchema) -> dict:
    async with async_session() as session:
        result = await session.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        todo = result.scalar_one_or_none()

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
            "priority": todo.priority
        }

# Delete todos by filter status
@delete("/todos", status_code=200)
async def delete_todos_by_status(status: str = "all") -> dict:
    async with async_session() as session:
        query = sql_delete(Todo)

        if status == "completed":
            query = query.where(Todo.completed == True)
        elif status == "active":
            query = query.where(Todo.completed == False)
       
        result = await session.execute(query)
        await session.commit()

        return {
            "message": "Todos deleted successfully",
            "deleted_count": result.rowcount
        }

# Delete one todo
@delete("/todos/{todo_id:int}", status_code=200)
async def delete_todo(todo_id: int) -> dict:
    async with async_session() as session:
        result = await session.execute(
            sql_delete(Todo).where(Todo.id == todo_id)
        )

        await session.commit()

        if result.rowcount == 0:
            raise NotFoundException("Todo not found")

        return {
            "message": "Todo deleted successfully"
        }


app = Litestar(
    route_handlers=[
        get_todos,
        add_todo,
        update_todo,
        delete_todos_by_status,
        delete_todo
    ],
    on_startup=[create_tables],
    cors_config=cors_config
)
