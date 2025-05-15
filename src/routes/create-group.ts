import { json } from '@sveltejs/kit';
import { createGroup } from '$lib';

export async function POST({ request }) {
  const { userId, token } = await request.json();
  try {
    const response = await createGroup(userId, token);
    return json(response);
  } catch (e) {
    return json({ error: 'Failed to create group' }, { status: 500 });
  }
}

