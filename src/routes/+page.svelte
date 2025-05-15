<script lang="ts">
  import { login } from '$lib';
  import { writable } from 'svelte/store';
  import GroupList from '$components/GroupList.svelte';
  import RoomList from '$components/RoomList.svelte';

  let email = '';
  let password = '';
  let error = '';
  const token = writable<string | null>(null);

  const handleLogin = async () => {
    try {
      const response = await login(email, password);
      token.set(response.token); // Simpan token
    } catch (e) {
      error = 'Login failed';
    }
  };
</script>

{#if $token}
  <div>
    <h2>Groups</h2>
    <GroupList {groups} />
    <h2>Rooms</h2>
    <RoomList {rooms} />
  </div>
{:else}
  <form on:submit|preventDefault={handleLogin}>
    <input type="email" bind:value={email} placeholder="Email" />
    <input type="password" bind:value={password} placeholder="Password" />
    <button type="submit">Login</button>
  </form>

  {#if error}
    <p>{error}</p>
  {/if}
{/if}
