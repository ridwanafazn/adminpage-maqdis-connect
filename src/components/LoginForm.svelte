<script lang="ts">
  import { login } from '$lib';
  export let onLogin: (token: string) => void;

  let email = '';
  let password = '';
  let error = '';

  const handleLogin = async () => {
    try {
      const response = await login(email, password);
      onLogin(response.token);
    } catch (e) {
      error = 'Login failed';
    }
  };
</script>

<form on:submit|preventDefault={handleLogin}>
  <input type="email" bind:value={email} placeholder="Email" />
  <input type="password" bind:value={password} placeholder="Password" />
  <button type="submit">Login</button>
</form>

{#if error}
  <p>{error}</p>
{/if}
