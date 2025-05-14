import { json } from '@sveltejs/kit';
import { login } from '$lib/api';

export async function POST({ request }) {
	const { baseUrl, email, password } = await request.json();

	try {
		const result = await login(baseUrl, email, password);
		return json(result);
	} catch (err) {
		return new Response(JSON.stringify({ error: 'Login gagal' }), { status: 400 });
	}
}