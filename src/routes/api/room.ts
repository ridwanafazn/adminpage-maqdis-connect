import { json } from '@sveltejs/kit';
import { getRooms } from '$lib';

export async function GET({ request }) {
  const token = request.headers.get('Authorization');
  try {
    const rooms = await getRooms(token);
    return json(rooms);
  } catch (e) {
    return json({ error: 'Failed to fetch rooms' }, { status: 500 });
  }
}
