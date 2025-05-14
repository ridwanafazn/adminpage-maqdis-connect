import { json } from '@sveltejs/kit';
import { getRooms } from '$lib/api';

export async function GET({ request }) {
	const { baseUrl, token } = await request.json();

	try {
		const rooms = await getRooms(baseUrl, token);
		return json(rooms);
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Gagal mengambil data room' }), { status: 400 });
	}
}
