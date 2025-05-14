<script lang="ts">
	import { session } from '$lib/stores/session';
	import { onMount } from 'svelte';
	import { createGroup } from '$lib/api';
	let groupName = '';
	let error = '';
	let successMessage = '';

	onMount(() => {
		const sessionData = $session;
		if (!sessionData.token || !sessionData.baseUrl) {
			error = 'Login diperlukan';
		}
	});

	async function handleCreateGroup() {
		const sessionData = $session;
		if (!sessionData.token || !sessionData.baseUrl) {
			error = 'Login diperlukan';
			return;
		}

		try {
			const data = await createGroup(sessionData.baseUrl, sessionData.token, sessionData.userId, groupName);
			successMessage = `Grup "${data.groupData.data.nama_grup}" berhasil dibuat!`;
		} catch (err) {
			error = 'Gagal membuat grup dan room';
		}
	}
</script>

{#if error}
	<p style="color: red">{error}</p>
{:else if successMessage}
	<p style="color: green">{successMessage}</p>
{:else}
	<div>
		<h3>Buat Grup Baru</h3>
		<label for="groupName">Nama Grup:</label>
		<input type="text" id="groupName" bind:value={groupName} placeholder="Masukkan nama grup" />
		<button on:click={handleCreateGroup}>Buat Grup</button>
	</div>
{/if}
