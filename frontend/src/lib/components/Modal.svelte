<script lang="ts">
  import type { Snippet } from "svelte";

  let { children }: { children: Snippet } = $props();
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center">
  <div
    class="w-[90%] max-w-md rounded-3xl border border-light-border bg-light-surface p-5 font-body text-light-text shadow-lg dark:border-dark-border dark:bg-dark-surface dark:text-dark-text"
  >
    {@render children()}
  </div>
</div>