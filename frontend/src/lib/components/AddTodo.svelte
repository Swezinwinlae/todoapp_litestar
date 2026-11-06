<script lang="ts">
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { addTodo } from "../todo_api/api";

  let { onClose }: { onClose: () => void } = $props();

  const queryClient = useQueryClient();

  let title = $state("");
  let description = $state("");
  let priority = $state<"High" | "Medium" | "Low">("Medium");

  const mutation = createMutation(() => ({
    mutationFn: addTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      onClose();
    },
  }));

  function submit() {
    mutation.mutate({ title, description, priority });
  }
</script>

<input bind:value={title} placeholder="Title" />
<input bind:value={description} placeholder="Description" />

<select bind:value={priority}>
  <option>High</option>
  <option>Medium</option>
  <option>Low</option>
</select>

<button onclick={submit} disabled={mutation.isPending}>Add</button>
<button onclick={onClose}>Cancel</button>