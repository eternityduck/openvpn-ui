'use client';
import React, { useEffect, useState } from 'react';
import { apiService } from '@/api/api';
import { User } from '@/models/user';
import styles from './UserList.module.css';
import ActionButton from '@/app/components/ActionButton';
import { useRouter } from 'next/navigation';

const UserListPage: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [showCreateUserForm, setShowCreateUserForm] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [showForm, setShowForm] = useState<boolean>(false);
    const [success, setSuccess] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState<string>('');

    const router = useRouter();

    const passwordAuth = process.env.NEXT_PUBLIC_AUTH_PASS === 'true';
    useEffect(() => {
        console.log(passwordAuth);
        const fetchData = async () => {
            try {
                const data = await apiService.getUsers();
                setUsers(data);
            } catch (error) {
                setError((error as Error).message);
            }
        };

        void fetchData();
        const interval = setInterval(fetchData, 20000);
        return () => clearInterval(interval);
    }, []);

    const handleRevoke = async (username: string) => {
        const success = await apiService.revokeUser(username);
        if (success) {
            setUsers(users.map((user) => (user.username === username ? { ...user, revoked: true } : user)));
        } else {
            alert('Failed to revoke user');
        }
    };

    const handleRatify = async (username: string) => {
        const success = await apiService.ratifyUser(username);
        if (success) {
            setUsers(users.map((user) => (user.username === username ? { ...user, revoked: false } : user)));
        } else {
            alert('Failed to ratify user');
        }
    };

    const handleDownload = async (username: string) => {
        await apiService.downloadConfig(username);
    };

    const handleCreateUser = async () => {
        if (!username.trim()) {
            setErrorMessage('Username cannot be empty.');
            setTimeout(() => setErrorMessage(null), 3000);
            return;
        }
        const existingUser = users.find((user) => user.username === username);
        if (existingUser) {
            setErrorMessage('User already exists!');
            setTimeout(() => setErrorMessage(null), 3000); // Hide error message after 3 seconds
            return;
        }

        const success = await apiService.createUser(username, passwordAuth ? password : undefined);
        if (success) {
            setShowCreateUserForm(false);
            setSuccessMessage('User created successfully!');
            const data = await apiService.getUsers();
            setUsers(data);
            setTimeout(() => setSuccessMessage(null), 3000);
        } else {
            setErrorMessage('User already exists!');
            setTimeout(() => setErrorMessage(null), 3000);
        }
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    const toggleForm = () => {
        setShowForm(!showForm);
    };

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
    };

    const filteredUsers = users.filter((user) => user.username.toLowerCase().includes(searchTerm.toLowerCase()));

    return (
        <div className={styles.container}>
            <h1>Users</h1>
            <button className={styles.goToGroupsButton} onClick={() => router.push('/groups')}>
                Go to Groups
            </button>
            <button className={styles.createButton} onClick={() => setShowCreateUserForm(true)}>
                Create User
            </button>
            <input
                type="text"
                placeholder="Search Users"
                value={searchTerm}
                onChange={handleSearchChange}
                className={styles.searchInput}
            />
            {showCreateUserForm && (
                <div className={styles.createUserForm}>
                    <h2>Create User</h2>
                    <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                    {passwordAuth && (
                        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    )}
                    <button onClick={handleCreateUser}>Submit</button>
                    <button onClick={() => setShowCreateUserForm(false)}>Cancel</button>
                </div>
            )}
            {errorMessage && <div className={styles.errorMessage}>{errorMessage}</div>}
            {successMessage && <div className={styles.successMessage}>{successMessage}</div>}
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Connected</th>
                        <th>Connected Since</th>
                        <th>Revoked</th>
                        <th>Revocation Date</th>
                        <th>Expiration Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredUsers.map((user) => (
                        <tr key={user.username} className={user.revoked ? styles.revoked : ''}>
                            <td>{user.username}</td>
                            <td className={user.connected ? styles.connected : ''}>{user.connected ? 'Yes' : 'No'}</td>
                            <td>{user.connected_since}</td>
                            <td>{user.revoked ? 'Yes' : 'No'}</td>
                            <td>{user.revocation_date}</td>
                            <td>{user.expiration_date}</td>
                            <td>
                                {user.revoked ? (
                                    <ActionButton onClick={() => handleRatify(user.username)} label="Ratify" type="ratify" />
                                ) : (
                                    <ActionButton onClick={() => handleRevoke(user.username)} label="Revoke" type="revoke" />
                                )}
                                <ActionButton onClick={() => handleDownload(user.username)} label="Download Config" type="download" />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default UserListPage;
