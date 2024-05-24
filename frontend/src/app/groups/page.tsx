'use client';

import React, { useEffect, useState } from 'react';
import { apiService } from '@/api/api';
import { useRouter } from 'next/navigation';
import styles from './Groups.module.css';
import { Group } from '@/models/group';

const GroupsPage = () => {
  const [groups, setGroups] = useState<Group[]>([]);

  const router = useRouter();

  useEffect(() => {
    apiService.getGroups().then(setGroups);
    console.log(groups);
  }, [apiService]);

  const handleShowGroup = (groupName: string) => {
    router.push(`/groups/${groupName}`);
  };

  const handleDeleteGroup = async (groupName: string) => {
    await apiService.deleteGroup(groupName);
    setGroups(groups.filter((group) => group.name !== groupName));
  };

  const handleAddRoute = (groupName: string) => {};

  const handleAddUser = (groupName: string) => {};

  return (
    <div className={styles.container}>
      <h1>Groups</h1>
      <button onClick={() => router.push('/')}>Go to Users</button>
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
                <button className={`${styles.button} ${styles.showButton}`} onClick={() => handleShowGroup(group.name)}>
                  Show
                </button>
                <button className={`${styles.button} ${styles.deleteButton}`} onClick={() => handleDeleteGroup(group.name)}>
                  Delete
                </button>
                <button className={`${styles.button} ${styles.addButton}`} onClick={() => handleAddRoute(group.name)}>
                  Add Route
                </button>
                <button className={`${styles.button} ${styles.addButton}`} onClick={() => handleAddUser(group.name)}>
                  Add User
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
