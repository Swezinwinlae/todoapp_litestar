export type Priority = "High" | "Medium" | "Low";

export type Filter = "all" | "active" | "completed";

export interface Todo {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: Priority;
}

export interface NewTodo {
  title: string;
  description?: string | null;
  completed?: boolean;
  priority?: Priority;
}

export interface UpdateTodo {
  title?: string;
  description?: string | null;
  completed?: boolean;
  priority?: Priority;
}