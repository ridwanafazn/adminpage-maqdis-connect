import { json } from '@sveltejs/kit';
import { login } from '$lib';

export async function POST({ request }) {
  const { email, password } = await request.json();
  try {
    const data = await login(email, password);
    return json(data);
  } catch (e) {
    return json({ error: 'Login failed' }, { status: 500 });
  }
}
