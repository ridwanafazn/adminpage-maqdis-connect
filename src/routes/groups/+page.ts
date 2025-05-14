import { json } from '@sveltejs/kit';
import { getGroups } from '$lib/api';

export async function GET({ request }) {
	const { baseUrl, token } = await request.json();

	try {
		const groups = await getGroups(baseUrl, token);
		return json(groups);
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Gagal mengambil data grup' }), { status: 400 });
	}
}
