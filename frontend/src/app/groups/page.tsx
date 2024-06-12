'use client';

import React, { useEffect, useState } from 'react';
import { apiService } from '@/api/api';
import { useRouter } from 'next/navigation';
import styles from './Groups.module.css';
import { Group } from '@/models/group';

const GroupsPage = () => {
    const [groups, setGroups] = useState<Group[]>([]);
    const [newGroupName, setNewGroupName] = useState<string>('');
    const [showForm, setShowForm] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const router = useRouter();

    useEffect(() => {
        apiService.getGroups().then(setGroups);
        console.log(groups);
    }, [apiService]);

    const handleDeleteGroup = async (groupName: string) => {
        await apiService.deleteGroup(groupName);
        setGroups(groups.filter((group) => group.name !== groupName));
    };

    const fetchGroups = () => {
        apiService
            .getGroups()
            .then((data) => setGroups(data))
            .catch((error) => setError(error.message));
    };

    const handleCreateGroup = () => {
        if (!newGroupName.trim()) {
            setError('Group name cannot be empty.');
            setTimeout(() => setError(null), 3000);
            return;
        }

        apiService
            .createGroup(newGroupName)
            .then(() => {
                setNewGroupName('');
                setShowForm(false);
                setSuccess('Group created successfully.');
                setTimeout(() => setSuccess(null), 3000);
                fetchGroups();
            })
            .catch((error) => {
                setError(error.message);
                setTimeout(() => setError(null), 3000);
            });
    };

    const toggleForm = () => {
        setShowForm(!showForm);
    };

    return (
        <div className={styles.container}>
            <h1>Groups</h1>
            <button className={styles.goToUsersButton} onClick={() => router.push('/')}>
                Go to Users
            </button>
            {error && <div className={styles.error}>{error}</div>}
            {success && <div className={styles.success}>{success}</div>}
            <button className={styles.createButton} onClick={toggleForm}>
                {showForm ? 'Cancel' : 'Create Group'}
            </button>
            {showForm && (
                <div className={styles.createForm}>
                    <input
                        type="text"
                        placeholder="Group Name"
                        value={newGroupName}
                        onChange={(e) => setNewGroupName(e.target.value)}
                    />
                    <button className={`${styles.button} ${styles.createButton}`} onClick={handleCreateGroup}>
                        Create
                    </button>
                </div>
            )}
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {groups.map((group) => (
                        <tr key={group.name}>
                            <td>{group.name}</td>
                            <td>
                                <button
                                    className={`${styles.button} ${styles.deleteButton}`}
                                    onClick={() => handleDeleteGroup(group.name)}
                                >
                                    Delete
                                </button>
                                <button
                                    className={`${styles.button} ${styles.addButton}`}
                                    onClick={() => router.push(`/groups/${group.name}/editRoutes`)}
                                >
                                    Edit Routes
                                </button>
                                <button
                                    className={`${styles.button} ${styles.addButton}`}
                                    onClick={() => router.push(`/groups/${group.name}/editUsers`)}
                                >
                                    Edit Users
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default GroupsPage;
