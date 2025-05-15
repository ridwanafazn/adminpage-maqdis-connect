<script lang="ts">
  import { createGroup } from '$lib';
  let userId = '';
  let error = '';
  export let token: string;

  const handleCreateGroup = async () => {
    try {
      const response = await createGroup(userId, token);
      console.log('Group created:', response);
    } catch (e) {
      error = 'Failed to create group';
    }
  };
</script>

<form on:submit|preventDefault={handleCreateGroup}>
  <input type="text" bind:value={userId} placeholder="User ID" />
  <button type="submit">Create Group</button>
</form>

{#if error}
  <p>{error}</p>
{/if}
