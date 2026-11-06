import axios from "axios";
import type { Todo, NewTodo, UpdateTodo, Filter } from "../types";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Get all todos
export async function getTodos(): Promise<Todo[]> {
  const response = await api.get("/todos");
  return response.data;
}

// Create a new todo
export async function addTodo(data: NewTodo): Promise<Todo> {
  const response = await api.post("/todos", data);
  return response.data;
}

// Update one todo
export async function updateTodo(id: number, data: UpdateTodo): Promise<Todo> {
  const response = await api.patch(`/todos/${id}`, data);
  return response.data;
}

// Delete one todo
export async function deleteTodo(id: number): Promise<void> {
  await api.delete(`/todos/${id}`);
}

// Delete todos by filter status
export async function deleteTodosByStatus(status: Filter): Promise<void> {
  await api.delete("/todos", { params: { status } });
}