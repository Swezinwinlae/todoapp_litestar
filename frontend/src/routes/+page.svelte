<script lang="ts">
  import SunFillIcon from "~icons/akar-icons/sun-fill";
  import MoonFillIcon from "~icons/akar-icons/moon-fill";

  import { createQuery, createMutation, useQueryClient } from "@tanstack/svelte-query";
  import toast, { Toaster } from "svelte-5-french-toast";
  import { getTodos, deleteTodo, deleteTodosByStatus } from "../lib/todo_api/api";
  import type { Todo, Filter } from "../lib/types";
  import TodoItem from "../lib/components/TodoItem.svelte";
  import TodoModal from "../lib/components/EditTodo.svelte";
  import ConfirmModal from "../lib/components/DeleteConfirm.svelte";

  const queryClient = useQueryClient();

  let openDarkMode = $state(false);
  let openSelectedFilter = $state(false);
  let selectedFilter = $state<Filter>("all");
  const filters: Filter[] = ["all", "active", "completed"];

  let showAdd = $state(false);
  let editingTodo = $state<Todo | null>(null);
  let deletingTodo = $state<Todo | null>(null);
  let showClear = $state(false);

  const todosQuery = createQuery(() => ({
    queryKey: ["todos"],
    queryFn: getTodos,
  }));

  let visibleTodos = $derived(
    (todosQuery.data ?? []).filter((t) => {
      if (selectedFilter === "active") return !t.completed;
      if (selectedFilter === "completed") return t.completed;
      return true;
    })
  );

  const deleteOne = createMutation(() => ({
    mutationFn: (id: number) => deleteTodo(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      toast.success("Todo deleted");
      deletingTodo = null;
    },
    onError: () => toast.error("Something went wrong"),
  }));

  const deleteMany = createMutation(() => ({
    mutationFn: () => deleteTodosByStatus(selectedFilter),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      toast.success("Todos deleted");
      showClear = false;
    },
    onError: () => toast.error("Something went wrong"),
  }));

  function toggleDarkMode() {
    openDarkMode = !openDarkMode;
  }

  function chooseFilter(option: Filter) {
    selectedFilter = option;
    openSelectedFilter = false;
  }
</script>

<div
  class:dark={openDarkMode}
  class="relative min-h-screen w-full bg-light-background bg-[url(/img/light_bg.jpg)] bg-no-repeat bg-top bg-size-[100%_300px] font-body text-light-text dark:bg-dark-background dark:bg-[url(/img/dark_bg.jpg)] dark:text-dark-text"
>
  <main class="mx-auto max-w-md px-4 pb-28 pt-16">
    <div class="mb-4 flex items-center justify-between">
      <h1 class="font-heading text-5xl font-bold tracking-wide text-light-text dark:text-dark-text">
        ToDo
      </h1>
      <button
        onclick={toggleDarkMode}
        class="text-light-text dark:text-dark-text"
        aria-label="Toggle dark mode"
      >
        {#if openDarkMode}
          <MoonFillIcon class="h-8 w-8" />
        {:else}
          <SunFillIcon class="h-8 w-8" />
        {/if}
      </button>
    </div>

    <div class="mb-4 flex items-center justify-between">
      <button
        onclick={() => (showAdd = true)}
        class="rounded-full bg-light-primary px-4 py-2 font-semibold text-light-text hover:bg-light-primary-hover dark:bg-dark-primary dark:text-dark-background dark:hover:bg-dark-primary-hover"
      >
        Add Todo
      </button>

      <div class="relative w-28">
        <button
          onclick={() => (openSelectedFilter = !openSelectedFilter)}
          aria-expanded={openSelectedFilter}
          class="w-full rounded-full bg-light-primary px-4 py-2 font-semibold capitalize text-light-text hover:bg-light-primary-hover dark:bg-dark-primary dark:text-dark-background dark:hover:bg-dark-primary-hover"
        >
          {selectedFilter}
        </button>

        {#if openSelectedFilter}
          <div
            class="absolute left-0 top-full z-10 mt-2 w-full overflow-hidden rounded-2xl bg-light-primary font-semibold text-light-text shadow-lg dark:bg-dark-primary dark:text-dark-background"
          >
            {#each filters as filter}
              <button
                onclick={() => chooseFilter(filter)}
                class="block w-full px-4 py-2 text-center capitalize hover:bg-light-primary-hover dark:hover:bg-dark-primary-hover"
              >
                {filter}
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <div
      class="overflow-hidden rounded-2xl border border-light-border bg-light-surface shadow-lg dark:border-dark-border dark:bg-dark-surface"
    >
      {#if todosQuery.isPending}
        <p class="p-5 text-center text-2xl font-semibold text-light-text-secondary dark:text-dark-text-secondary">Loading...</p>
      {:else if todosQuery.isError}
        <p class="p-5 text-center text-2xl font-semibold text-light-text-secondary dark:text-dark-text-secondary">
          Something went wrong
        </p>
      {:else}
        {#each visibleTodos as todo (todo.id)}
          <TodoItem
            {todo}
            onEdit={() => (editingTodo = todo)}
            onDelete={() => (deletingTodo = todo)}
          />
        {:else}
          <p class="p-5 text-center text-2xl font-semibold text-light-text-secondary dark:text-dark-text-secondary">No todos</p>
        {/each}
      {/if}

      <div
        class="flex justify-between p-4 text-sm text-light-text-secondary dark:text-dark-text-secondary"
      >
        <span>{visibleTodos.length} items</span>
        <button
          class="capitalize hover:text-light-text disabled:opacity-50 dark:hover:text-dark-text"
          onclick={() => (showClear = true)}
          disabled={visibleTodos.length === 0}
        >
          Delete {selectedFilter}
        </button>
      </div>
    </div>
  </main>

  {#if showAdd}
    <TodoModal onClose={() => (showAdd = false)} />
  {/if}

  {#if editingTodo}
    <TodoModal todo={editingTodo} onClose={() => (editingTodo = null)} />
  {/if}

  {#if deletingTodo}
    <ConfirmModal
      message={`Delete "${deletingTodo.title}"?`}
      onConfirm={() => deleteOne.mutate(deletingTodo!.id)}
      onCancel={() => (deletingTodo = null)}
    />
  {/if}

  {#if showClear}
    <ConfirmModal
      message={`Delete ${selectedFilter} todos? This cannot be undone.`}
      onConfirm={() => deleteMany.mutate()}
      onCancel={() => (showClear = false)}
    />
  {/if}
</div>

<Toaster />