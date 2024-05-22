import {User} from "@/models/user";

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

    async createUser(data: Partial<User>): Promise<User> {
        return await this.fetch<User>('/users', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async deleteUser(userId: string): Promise<void> {
        await this.fetch<void>(`/users/${userId}`, {
            method: 'DELETE',
        });
    }

    // Add more methods as needed
}

export const apiService = new ApiService('http://127.0.0.1:8080');