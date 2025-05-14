<script lang="ts">
	import { session } from '$lib/stores/session';
	import { goto } from '$app/navigation';

	let baseUrl = '';
	let email = '';
	let password = '';
	let error = '';

	async function handleLogin() {
		try {
			const res = await fetch('/login', {
				method: 'POST',
				body: JSON.stringify({ baseUrl, email, password })
			});

			if (!res.ok) {
				error = 'Login gagal';
				return;
			}

			const data = await res.json();
			session.set({
				baseUrl,
				token: data.token,
				userId: data.id,
				username: data.username,
				email: data.email
			});
			goto('/dashboard'); // halaman setelah login
		} catch (err) {
			error = 'Terjadi kesalahan';
		}
	}
</script>

<form on:submit|preventDefault={handleLogin}>
	<input type="text" bind:value={baseUrl} placeholder="Base URL" required />
	<input type="email" bind:value={email} placeholder="Email" required />
	<input type="password" bind:value={password} placeholder="Password" required />
	<button type="submit">Login</button>
</form>

{#if error}
	<p style="color: red">{error}</p>
{/if}
