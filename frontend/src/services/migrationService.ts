/**
 * Migration service
 */
import apiClient from './api';

export interface MigrationConfig {
    direction: string;
    mode: string;
    entities: string[];
    batch_size?: number;
    optimize_images?: boolean;
    generate_redirects?: boolean;
}

export interface MigrationJob {
    id: string;
    direction: string;
    mode: string;
    status: string;
    progress: number;
    total_items: number;
    migrated_items: number;
    failed_items: number;
    created_at: string;
    started_at?: string;
    completed_at?: string;
}

export const migrationService = {
    /**
     * Start a new migration
     */
    async startMigration(config: MigrationConfig): Promise<{ job_id: string; status: string; message: string }> {
        const response = await apiClient.post('/migration/start', config);
        return response.data;
    },

    /**
     * Get all migration jobs
     */
    async getMigrationJobs(skip: number = 0, limit: number = 20): Promise<MigrationJob[]> {
        const response = await apiClient.get('/migration/jobs', {
            params: { skip, limit },
        });
        return response.data;
    },

    /**
     * Get single migration job
     */
    async getMigrationJob(jobId: string): Promise<MigrationJob> {
        const response = await apiClient.get(`/migration/jobs/${jobId}`);
        return response.data;
    },

    /**
     * Cancel migration job
     */
    async cancelMigration(jobId: string): Promise<{ message: string }> {
        const response = await apiClient.post(`/migration/jobs/${jobId}/cancel`);
        return response.data;
    },

    /**
     * Test API connections
     */
    async testConnections(): Promise<{
        shopify: { connected: boolean; configured: boolean };
        woocommerce: { connected: boolean; configured: boolean };
    }> {
        const response = await apiClient.get('/products/test-connection');
        return response.data;
    },
};

export default migrationService;
