export interface User {
    username: string;
    connected: boolean;
    connected_since: string | null;
    revoked: boolean;
    revocation_date: string | null;
    expiration_date: string | null;
}