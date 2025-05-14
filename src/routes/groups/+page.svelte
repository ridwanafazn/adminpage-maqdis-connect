<script lang="ts">
	import { session } from '$lib/stores/session';
	import { onMount } from 'svelte';
	let groups = [];
	let error = '';

	onMount(async () => {
		const sessionData = $session;
		if (!sessionData.token || !sessionData.baseUrl) {
			error = 'Login diperlukan';
			return;
		}

		try {
			const data = await fetchGroups(sessionData.baseUrl, sessionData.token);
			groups = data;
		} catch (err) {
			error = 'Gagal mengambil data grup';
		}
	});

	async function fetchGroups(baseUrl: string, token: string) {
		const res = await fetch(`${baseUrl}/api/Group`, {
			headers: { 'Authorization': `Bearer ${token}` }
		});
		const data = await res.json();
		return data;
	}
</script>

{#if error}
	<p style="color: red">{error}</p>
{:else}
	<ul>
		{#each groups as group}
			<li>{group.nama_grup} - {group.created_by}</li>
		{/each}
	</ul>
{/if}
