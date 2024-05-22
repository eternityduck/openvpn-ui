// app/users/page.tsx
'use client'
import React, { useEffect, useState } from 'react';
import {apiService} from "@/api/api";
import {User} from "@/models/user";
import styles from './UserList.module.css'; // Assume you have some basic styles

const UserListPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await apiService.getUsers();
        setUsers(data);
      } catch (error) {
        setError((error as Error).message);
      }
    };

    void fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleRevoke = async (username: string) => {
    await apiService.revokeUser(username);
    setUsers(users.map(user => user.username === username ? { ...user, revoked: true } : user));
  };

  const handleRatify = async (username: string) => {
    await apiService.ratifyUser(username);
    setUsers(users.map(user => user.username === username ? { ...user, revoked: false } : user));
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
      <div className={styles.container}>
        <h1>User List</h1>
        <button className={styles.createButton}>Create User</button>
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
          {users.map(user => (
              <tr key={user.username} className={user.revoked ? styles.revoked : ''}>
                <td>{user.username}</td>
                <td className={user.connected ? styles.connected : ''}>
                  {user.connected ? 'Yes' : 'No'}
                </td>
                <td>{user.connected_since}</td>
                <td>{user.revoked ? 'Yes' : 'No'}</td>
                <td>{user.revocation_date}</td>
                <td>{user.expiration_date}</td>
                <td>
                  {user.revoked ? (
                      <button onClick={() => handleRatify(user.username)}>Ratify</button>
                  ) : (
                      <button onClick={() => handleRevoke(user.username)}>Revoke</button>
                  )}
                </td>
              </tr>
          ))}
          </tbody>
        </table>
      </div>
  );
};

export default UserListPage;
