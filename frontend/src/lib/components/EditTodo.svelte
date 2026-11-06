<script lang="ts">
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import toast from "svelte-5-french-toast";
  import { addTodo, updateTodo } from "../todo_api/api";
  import type { Todo, Priority, NewTodo } from "../types";
  import Modal from "./Modal.svelte";

  let { todo = null, onClose }: { todo?: Todo | null; onClose: () => void } = $props();

  const queryClient = useQueryClient();

  let title = $state("");
  let description = $state("");
  let priority = $state<Priority>("Medium");

  $effect(() => {
    title = todo?.title ?? "";
    description = todo?.description ?? "";
    priority = todo?.priority ?? "Medium";
  });

  const mutation = createMutation(() => ({
    mutationFn: () => {
      const data: NewTodo = { title, description, priority };
      return todo ? updateTodo(todo.id, data) : addTodo(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      toast.success(todo ? "Todo updated" : "Todo added");
      onClose();
    },
    onError: () => toast.error("Something went wrong"),
  }));
</script>

<Modal>
  <h2 class="mb-4 font-heading text-2xl font-semibold">
    {todo ? "Edit todo" : "New todo"}
  </h2>

  <input
    class="mb-3 w-full rounded-lg bg-light-secondary p-3 text-light-text outline-none placeholder:text-light-text-secondary dark:bg-dark-secondary dark:text-dark-text dark:placeholder:text-dark-text-secondary"
    placeholder="Add todo title..."
    bind:value={title}
  />
  <input
    class="mb-4 w-full rounded-lg bg-light-secondary p-3 text-light-text outline-none placeholder:text-light-text-secondary dark:bg-dark-secondary dark:text-dark-text dark:placeholder:text-dark-text-secondary"
    placeholder="Add description..."
    bind:value={description}
  />

  <div class="flex items-center justify-between">
    <select
      class="rounded-lg bg-light-secondary p-3 text-light-text dark:bg-dark-secondary dark:text-dark-text"
      bind:value={priority}
    >
      <option>High</option>
      <option>Medium</option>
      <option>Low</option>
    </select>

    <div class="flex items-center gap-3">
      <button
        onclick={onClose}
        class="text-light-text-secondary hover:text-light-text dark:text-dark-text-secondary dark:hover:text-dark-text"
      >
        Cancel
      </button>
      <button
        onclick={() => mutation.mutate()}
        disabled={!title.trim() || mutation.isPending}
        class="rounded-full bg-light-primary px-6 py-2 font-semibold text-light-text hover:bg-light-primary-hover disabled:opacity-50 dark:bg-dark-primary dark:text-dark-background dark:hover:bg-dark-primary-hover"
      >
        {todo ? "Save" : "Add"}
      </button>
    </div>
  </div>
</Modal>