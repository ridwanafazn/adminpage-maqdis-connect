import { json } from '@sveltejs/kit';
import { createGroup } from '$lib/api';

export async function POST({ request }) {
	const { baseUrl, token, userId, groupName } = await request.json();

	try {
		const data = await createGroup(baseUrl, token, userId, groupName);
		return json(data);
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Gagal membuat grup dan room' }), { status: 400 });
	}
}
