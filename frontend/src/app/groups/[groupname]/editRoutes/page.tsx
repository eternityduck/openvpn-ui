'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Group } from '@/models/group';
import { Route } from '@/models/route';
import { apiService } from '@/api/api';

import styles from './EditGroupRoutes.module.css';

const EditGroupRoutes = ({ params }: { params: { groupname: string } }) => {
    const router = useRouter();
    const { groupname } = params;
    const [group, setGroup] = useState<Group | null>(null);
    const [newRoute, setNewRoute] = useState<Route>({ address: '', mask: '' });
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    useEffect(() => {
        if (groupname) {
            apiService
                .getGroup(groupname as string)
                .then((data) => setGroup(data))
                .catch((error) => setError(error.message));
        }
    }, [groupname]);

    const handleAddRoute = () => {
        if (!groupname) return;
        if (!newRoute.address || !newRoute.mask) {
            setError('Both address and mask are required.');
            setTimeout(() => setError(null), 3000);
            return;
        }
        if (!validateIPAddress(newRoute.address) || !validateIPAddress(newRoute.mask)) {
            setError('Both address and mask must be in the format xxx.xxx.xxx.xxx, where xxx is a number from 0 to 255.');
            setTimeout(() => setError(null), 3000);
            return;
        }
        apiService
            .addRoutesToGroup(groupname as string, [newRoute])
            .then((data) => {
                const newRoutes = Array.isArray(data) ? data : [data];

                setGroup((prevGroup) => ({
                    ...prevGroup!,
                    routes: [...prevGroup!.routes, ...newRoutes],
                }));
                setNewRoute({ address: '', mask: '' });
                setSuccess('Route added successfully.');
                setTimeout(() => setSuccess(null), 3000);
            })
            .catch((error) => {
                setError(error.message);
                setTimeout(() => setError(null), 3000);
            });
    };

    const handleRemoveRoute = (address: string, mask: string) => {
        if (!groupname) return;
        apiService
            .removeRoutesFromGroup(groupname as string, [{ address, mask }])
            .then(() => {
                setGroup((prevGroup) => ({
                    ...prevGroup!,
                    routes: prevGroup!.routes.filter((route) => route.address !== address || route.mask !== mask),
                }));
                setSuccess('Route removed successfully.');
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

    const validateIPAddress = (ip: string) => {
        const ipRegex =
            /^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$/;
        return ipRegex.test(ip);
    };

    if (!group) return <div>Loading...</div>;

    return (
        <div>
            <button className={styles.goBackButton} onClick={handleGoBack}>
                Go Back to All Groups
            </button>
            <h1>Edit Routes for Group: {group.name}</h1>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            {success && <div style={{ color: 'green' }}>{success}</div>}
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Address</th>
                        <th>Mask</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {group.routes.map((route, index) => (
                        <tr key={index}>
                            <td>{route.address}</td>
                            <td>{route.mask}</td>
                            <td>
                                <button
                                    className={`${styles.button} ${styles.removeButton}`}
                                    onClick={() => handleRemoveRoute(route.address, route.mask)}
                                >
                                    Remove
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className={styles.addRouteForm}>
                <h2>Add Route</h2>
                <input
                    type="text"
                    placeholder="Address"
                    value={newRoute.address}
                    onChange={(e) => setNewRoute({ ...newRoute, address: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Mask"
                    value={newRoute.mask}
                    onChange={(e) => setNewRoute({ ...newRoute, mask: e.target.value })}
                />
                <button onClick={handleAddRoute}>Add Route</button>
            </div>
        </div>
    );
};

export default EditGroupRoutes;
