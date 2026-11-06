<script lang="ts">
  import Modal from "./Modal.svelte";

  let { message, onConfirm, onCancel }: {
    message: string;
    onConfirm: () => void;
    onCancel: () => void;
  } = $props();
</script>

<Modal>
  <h2 class="mb-2 font-heading text-2xl font-semibold">Are you sure?</h2>
  <p class="mb-5 text-light-text-secondary dark:text-dark-text-secondary">{message}</p>

  <div class="flex justify-end gap-3">
    <button
      onclick={onCancel}
      class="text-light-text-secondary hover:text-light-text dark:text-dark-text-secondary dark:hover:text-dark-text"
    >
      Cancel
    </button>
    <button
      onclick={onConfirm}
      class="rounded-full bg-red-600 px-6 py-2 font-semibold text-white hover:bg-red-700"
    >
      Delete
    </button>
  </div>
</Modal>