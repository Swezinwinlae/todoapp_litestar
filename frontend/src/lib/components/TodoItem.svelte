<script lang="ts">
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { updateTodo } from "../todo_api/api";
  import type { Todo, Priority } from "../types";
  import DeleteFilledIcon from "~icons/ant-design/delete-filled";
  import EditFilledIcon from "~icons/bitcoin-icons/edit-filled";
  import DetailsMoreIcon from "~icons/gg/details-more";
  import DetailsLessIcon from "~icons/gg/details-less";

  let { todo, onEdit, onDelete }: {
    todo: Todo;
    onEdit: () => void;
    onDelete: () => void;
  } = $props();

  const queryClient = useQueryClient();
  let showDetails = $state(false);

  const colors: Record<Priority, string> = {
    High: "bg-red-500",
    Medium: "bg-yellow-400",
    Low: "bg-green-500",
  };

  const toggle = createMutation(() => ({
    mutationFn: () => updateTodo(todo.id, { completed: !todo.completed }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["todos"] }),
  }));
</script>

<div class="border-b border-light-border bg-light-surface px-5 py-4 dark:bg-dark-secondary dark:border-dark-border">
  <div class="flex items-center gap-3">
    <input type="checkbox" checked={todo.completed} onchange={() => toggle.mutate()} />

    <span class="flex-1 {todo.completed ? 'text-light-text-secondary line-through dark:text-dark-text-secondary' : 'text-light-text dark:text-dark-text'}">
      {todo.title}
    </span>

    <span class="h-3 w-3 rounded-full {colors[todo.priority]}"></span>

    <button
      onclick={() => (showDetails = !showDetails)}
      class="text-light-text hover:text-light-text-secondary dark:text-dark-text dark:hover:text-dark-text-secondary"
      aria-label={showDetails ? "Hide details" : "Show details"}
    >
      {#if showDetails}
        <DetailsLessIcon class="h-6 w-6" />
      {:else}
        <DetailsMoreIcon class="h-6 w-6" />
      {/if}
    </button>
    <button
      onclick={onEdit}
      class="text-light-text hover:text-light-text-secondary dark:text-dark-text dark:hover:text-dark-text-secondary"
      aria-label="Edit"
    >
      <EditFilledIcon class="h-5 w-5" />
    </button>
    <button
      onclick={onDelete}
      class="text-light-text hover:text-light-text-secondary dark:text-dark-text dark:hover:text-dark-text-secondary"
      aria-label="Delete"
    >
      <DeleteFilledIcon class="h-5 w-5" />
    </button>
  </div>

  {#if showDetails}
    <div class="ml-8 mt-3 space-y-1 text-sm">
      <p><b>Description:</b> {todo.description || "No description"}</p>
      <p><b>Priority:</b> {todo.priority}</p>
    </div>
  {/if}
</div>