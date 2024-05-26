import { User } from '@/models/user';
import { Group } from '@/models/group';
import { Route } from '@/models/route';

class ApiService {
    baseURL: string;

    constructor(baseURL: string) {
        this.baseURL = baseURL;
    }

    async fetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async getUsers(): Promise<User[]> {
        return await this.fetch<User[]>('');
    }

    async downloadConfig(username: string): Promise<void> {
        const response = await fetch(`${this.baseURL}/download/${username}`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${username}.ovpn`);
        document.body.appendChild(link);
        link.click();
        link.remove();
    }

    async ratifyUser(username: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/ratify/${username}`, {
            method: 'GET',
        });
        return response.ok;
    }

    async revokeUser(username: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/revoke/${username}`, {
            method: 'GET',
        });
        return response.ok;
    }

    async createUser(username: string, password?: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        return response.ok;
    }

    async getGroups(): Promise<Group[]> {
        return await this.fetch<Group[]>('/groups');
    }

    async getGroup(groupName: string): Promise<Group> {
        return await this.fetch<Group>(`/groups/${groupName}`);
    }

    async createGroup(groupName: string): Promise<void> {
        if (groupName.trim() === '') {
            throw new Error('Group name cannot be empty');
        }
        const response = await fetch(`${this.baseURL}/groups`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: groupName }),
        });

        if (!response.ok) {
            throw new Error('Failed to create group');
        }
    }

    async deleteGroup(groupName: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/groups/${groupName}`, {
            method: 'DELETE',
        });
        return response.ok;
    }

    async addUserToGroup(groupName: string, username: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/groups/${groupName}/users/${username}`, {
            method: 'GET',
        });
        return response.ok;
    }

    async removeUserFromGroup(groupName: string, username: string): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/groups/${groupName}/users/${username}`, {
            method: 'DELETE',
        });
        return response.ok;
    }

    async getGroupUsers(groupName: string): Promise<string[]> {
        return await this.fetch<string[]>(`/groups/${groupName}/users`);
    }

    async addRoutesToGroup(groupName: string, routes: Route[]): Promise<Route[]> {
        const response = await fetch(`${this.baseURL}/groups/${groupName}/routes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(routes),
        });
        if (!response.ok) {
            throw new Error('Failed to add routes.');
        }
        return response.json();
    }

    async removeRoutesFromGroup(groupName: string, routes: Route[]): Promise<boolean> {
        const response = await fetch(`${this.baseURL}/groups/${groupName}/routes`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(routes),
        });
        if (!response.ok) {
            throw new Error('Failed to remove routes.');
        }
        return response.ok;
    }
}

export const apiService = new ApiService(`${process.env.NEXT_PUBLIC_API_HOST}:${process.env.NEXT_PUBLIC_API_PORT}`);
