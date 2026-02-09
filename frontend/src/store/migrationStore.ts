/**
 * Migration store using Zustand
 */
import { create } from 'zustand';
import migrationService, { type MigrationJob } from '../services/migrationService';

interface MigrationState {
    jobs: MigrationJob[];
    currentJob: MigrationJob | null;
    isLoading: boolean;
    fetchJobs: () => Promise<void>;
    fetchJob: (jobId: string) => Promise<void>;
    startMigration: (config: any) => Promise<string>;
    cancelMigration: (jobId: string) => Promise<void>;
}

export const useMigrationStore = create<MigrationState>((set) => ({
    jobs: [],
    currentJob: null,
    isLoading: false,

    fetchJobs: async () => {
        set({ isLoading: true });
        try {
            const jobs = await migrationService.getMigrationJobs();
            set({ jobs, isLoading: false });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    fetchJob: async (jobId: string) => {
        set({ isLoading: true });
        try {
            const job = await migrationService.getMigrationJob(jobId);
            set({ currentJob: job, isLoading: false });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    startMigration: async (config: any) => {
        set({ isLoading: true });
        try {
            const result = await migrationService.startMigration(config);
            set({ isLoading: false });
            return result.job_id;
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    cancelMigration: async (jobId: string) => {
        set({ isLoading: true });
        try {
            await migrationService.cancelMigration(jobId);
            set({ isLoading: false });
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },
}));

export default useMigrationStore;
