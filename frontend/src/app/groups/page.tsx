'use client';

import React, { useEffect, useState } from 'react';
import { apiService } from '@/api/api';
import { useRouter } from 'next/router';
import styles from './Groups.module.css';
import { Group } from '@/models/group';

const GroupsPage = () => {
  const [groups, setGroups] = useState<Group[]>([]);

  const router = useRouter();

  useEffect(() => {
    apiService.getGroups().then(setGroups);
  }, [apiService]);

  const handleShowGroup = (groupId: string) => {
    router.push(`/groups/${groupId}`);
  };

  const handleDeleteGroup = async (groupId: string) => {
    await apiService.deleteGroup(groupId);
    setGroups(groups.filter((group) => group.id !== groupId));
  };

  const handleAddRoute = (groupId: string) => {
    // Logic for adding a route
  };

  const handleAddUser = (groupId: string) => {
    // Logic for adding a user
  };

  return (
    <div>
      <h1>Groups</h1>
      <button onClick={() => router.push('/')}>Back to Users</button>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Group Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {groups.map((group) => (
            <tr key={group.id}>
              <td>{group.name}</td>
              <td>
                <button onClick={() => handleShowGroup(group.id)}>Show</button>
                <button onClick={() => handleDeleteGroup(group.id)}>Delete</button>
                <button onClick={() => handleAddRoute(group.id)}>Add Route</button>
                <button onClick={() => handleAddUser(group.id)}>Add User</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GroupsPage;
