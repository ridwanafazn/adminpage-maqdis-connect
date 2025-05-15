import { json } from '@sveltejs/kit';
import { getGroups } from '$lib';

export async function GET({ request }) {
  const token = request.headers.get('Authorization');
  try {
    const groups = await getGroups(token);
    return json(groups);
  } catch (e) {
    return json({ error: 'Failed to fetch groups' }, { status: 500 });
  }
}