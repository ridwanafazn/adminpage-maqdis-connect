export async function login(baseUrl: string, email: string, password: string) {
	const res = await fetch(`${baseUrl}/api/auth/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});

	if (!res.ok) throw new Error('Login gagal');
	const data = await res.json();
	return data;
}

export async function getGroups(baseUrl: string, token: string) {
	const res = await fetch(`${baseUrl}/api/Group`, {
		headers: {
			'Authorization': `Bearer ${token}`
		}
	});

	if (!res.ok) throw new Error('Gagal mengambil data grup');
	const data = await res.json();
	return data;
}

export async function getRooms(baseUrl: string, token: string) {
	const res = await fetch(`${baseUrl}/api/Audio/getRoom`, {
		headers: {
			'Authorization': `Bearer ${token}`
		}
	});

	if (!res.ok) throw new Error('Gagal mengambil data room');
	const data = await res.json();
	return data.getAllrooms; // Menyesuaikan dengan struktur respons
}

export async function createGroup(baseUrl: string, token: string, userId: string, groupName: string) {
	// 1. Buat grup dengan `/api/Group/admin?userId=...`
	const groupRes = await fetch(`${baseUrl}/api/Group/admin?userId=${userId}`, {
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ nama_grup: groupName })
	});

	if (!groupRes.ok) throw new Error('Gagal membuat grup');
	const groupData = await groupRes.json();

	// 2. Buat room dengan `/api/Audio/generateToken`
	const roomRes = await fetch(`${baseUrl}/api/Audio/generateToken`, {
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ nama_room: groupName })
	});

	if (!roomRes.ok) throw new Error('Gagal membuat room');
	const roomData = await roomRes.json();

	// 3. Assign room ke grup dengan `/api/Audio/assignRoom`
	const assignRes = await fetch(`${baseUrl}/api/Audio/assignRoom`, {
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			roomid: roomData.room.id,
			grupid: groupData.data.grupid
		})
	});

	if (!assignRes.ok) throw new Error('Gagal menugaskan room ke grup');
	
	// 4. Refresh token dengan `/api/Audio/refreshToken`
	const refreshRes = await fetch(`${baseUrl}/api/Audio/refreshToken`, {
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ room_Id: roomData.room.id })
	});

	if (!refreshRes.ok) throw new Error('Gagal menyegarkan token');
	const refreshData = await refreshRes.json();

	return { groupData, roomData, refreshData };
}
