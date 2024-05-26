'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiService } from '@/api/api';
import styles from './EditGroupUsers.module.css';

const EditGroupUsers = ({ params }: { params: { groupname: string } }) => {
    const router = useRouter();
    const { groupname } = params;
    const [groupUsers, setGroupUsers] = useState<string[]>([]);
    const [allUsers, setAllUsers] = useState<string[]>([]);
    const [newUsername, setNewUsername] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    useEffect(() => {
        if (groupname) {
            apiService
                .getGroupUsers(groupname)
                .then((data) => setGroupUsers(data))
                .catch((error) => setError(error.message));
        }

        apiService
            .getUsers()
            .then((data) => setAllUsers(data.map((user) => user.username)))
            .catch((error) => setError(error.message));
    }, [groupname]);

    const handleAddUser = () => {
        if (!newUsername.trim()) {
            setError('Username cannot be empty.');
            setTimeout(() => setError(null), 3000);
            return;
        }

        if (!allUsers.includes(newUsername)) {
            setError('User does not exist.');
            setTimeout(() => setError(null), 3000);
            return;
        }

        apiService
            .addUserToGroup(groupname, newUsername)
            .then(() => {
                setGroupUsers((prevUsers) => [...prevUsers, newUsername]);
                setNewUsername('');
                setSuccess('User added successfully.');
                setTimeout(() => setSuccess(null), 3000);
            })
            .catch((error) => {
                setError(error.message);
                setTimeout(() => setError(null), 3000);
            });
    };

    const handleRemoveUser = (username: string) => {
        apiService
            .removeUserFromGroup(groupname, username)
            .then(() => {
                setGroupUsers((prevUsers) => prevUsers.filter((user) => user !== username));
                setSuccess('User removed successfully.');
                setTimeout(() => setSuccess(null), 3000);
            })
            .catch((error) => {
                setError(error.message);
                setTimeout(() => setError(null), 3000);
            });
    };

    const handleGoBack = () => {
        router.push('/groups');
    };

    return (
        <div className={styles.container}>
            <button className={styles.goBackButton} onClick={handleGoBack}>
                Go Back to All Groups
            </button>
            <h1>Edit Users for Group: {groupname}</h1>
            {error && <div className={styles.errorMessage}>{error}</div>}
            {success && <div className={styles.successMessage}>{success}</div>}
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {groupUsers.map((username, index) => (
                        <tr key={index}>
                            <td>{username}</td>
                            <td>
                                <button
                                    className={`${styles.button} ${styles.removeButton}`}
                                    onClick={() => handleRemoveUser(username)}
                                >
                                    Remove
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className={styles.addUserForm}>
                <h2>Add User</h2>
                <input type="text" placeholder="Username" value={newUsername} onChange={(e) => setNewUsername(e.target.value)} />
                <button className={styles.addButton} onClick={handleAddUser}>
                    Add User
                </button>
            </div>
        </div>
    );
};

export default EditGroupUsers;
