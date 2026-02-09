/**
 * Authentication store using Zustand
 */
import { create } from 'zustand';
import authService, { type User } from '../services/authService';

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    fetchCurrentUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: authService.isAuthenticated(),
    isLoading: false,

    login: async (username: string, password: string) => {
        set({ isLoading: true });
        try {
            await authService.login({ username, password });
            const user = await authService.getCurrentUser();
            set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    logout: () => {
        authService.logout();
        set({ user: null, isAuthenticated: false });
    },

    fetchCurrentUser: async () => {
        set({ isLoading: true });
        try {
            const user = await authService.getCurrentUser();
            set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
            set({ user: null, isAuthenticated: false, isLoading: false });
            throw error;
        }
    },
}));

export default useAuthStore;
