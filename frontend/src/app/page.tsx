'use client';
import React, { useEffect, useState } from 'react';
import { apiService } from '@/api/api';
import { User } from '@/models/user';
import styles from './UserList.module.css';
import ActionButton from '@/app/components/ActionButton';
import { router } from 'next/client';

const UserListPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showCreateUserForm, setShowCreateUserForm] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordAuth, setPasswordAuth] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

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

  return (
    <div className={styles.container}>
      <h1>Users</h1>
      <button onClick={() => router.push('/groups')}>Go to Groups</button>
      <button className={styles.createButton} onClick={() => setShowCreateUserForm(true)}>
        Create User
      </button>
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
          {users.map((user) => (
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
