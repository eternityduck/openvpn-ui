import {User} from "@/models/user";
import {Group} from "@/models/group";

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

    async getUser(userId: string): Promise<User> {
        return await this.fetch<User>(`/users/${userId}`);
    }

    async deleteUser(userId: string): Promise<void> {
        await this.fetch<void>(`/users/${userId}`, {
            method: 'DELETE',
        });
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
        const response = await fetch(`${this.baseURL}/user`, {
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
}

export const apiService = new ApiService('http://127.0.0.1:8080');