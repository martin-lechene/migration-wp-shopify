/**
 * Authentication service
 */
import apiClient from './api';

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface TokenResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface User {
    id: string;
    email: string;
    username: string;
    full_name?: string;
    is_active: boolean;
    is_admin: boolean;
}

export const authService = {
    /**
     * Login with username and password
     */
    async login(credentials: LoginCredentials): Promise<TokenResponse> {
        // Create form data for OAuth2 password flow
        const formData = new FormData();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await apiClient.post<TokenResponse>('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        // Store tokens
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);

        return response.data;
    },

    /**
     * Get current user info
     */
    async getCurrentUser(): Promise<User> {
        const response = await apiClient.get<User>('/auth/me');
        return response.data;
    },

    /**
     * Logout
     */
    logout(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    },
};

export default authService;
