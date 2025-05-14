<script lang="ts">
	import { session } from '$lib/stores/session';
	import { onMount } from 'svelte';
	let rooms = [];
	let error = '';

	onMount(async () => {
		const sessionData = $session;
		if (!sessionData.token || !sessionData.baseUrl) {
			error = 'Login diperlukan';
			return;
		}

		try {
			const data = await fetchRooms(sessionData.baseUrl, sessionData.token);
			rooms = data;
		} catch (err) {
			error = 'Gagal mengambil data room';
		}
	});

	async function fetchRooms(baseUrl: string, token: string) {
		const res = await fetch(`${baseUrl}/api/Audio/getRoom`, {
			headers: { 'Authorization': `Bearer ${token}` }
		});
		const data = await res.json();
		return data.getAllrooms; // Menyesuaikan dengan struktur respons
	}
</script>

{#if error}
	<p style="color: red">{error}</p>
{:else}
	<ul>
		{#each rooms as room}
			<li>{room.nama_room} (ID: {room.id})</li>
		{/each}
	</ul>
{/if}
