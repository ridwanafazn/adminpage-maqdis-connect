import { writable } from 'svelte/store';

export const session = writable({
	baseUrl: '',
	token: '',
	userId: '',
	username: '',
	email: ''
});