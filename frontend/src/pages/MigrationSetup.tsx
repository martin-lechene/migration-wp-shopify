/**
 * Migration setup page
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useMigrationStore } from '@/store/migrationStore';
import Button from '@/components/common/Button';

export const MigrationSetup: React.FC = () => {
    const [direction, setDirection] = useState('shopify_to_woocommerce');
    const [mode, setMode] = useState('full');
    const [entities, setEntities] = useState<string[]>(['products']);
    const { startMigration } = useMigrationStore();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const jobId = await startMigration({
                direction,
                mode,
                entities,
                batch_size: 50,
                optimize_images: true,
                generate_redirects: false,
            });

            toast.success('Migration started successfully!');
            navigate(`/monitoring`);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to start migration');
        }
    };

    const toggleEntity = (entity: string) => {
        setEntities(prev =>
            prev.includes(entity)
                ? prev.filter(e => e !== entity)
                : [...prev, entity]
        );
    };

    return (
        <div className="max-w-3xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Setup New Migration</h1>
                <p className="text-gray-600">Configure your migration settings</p>
            </div>

            <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
                {/* Direction */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Migration Direction
                    </label>
                    <select
                        value={direction}
                        onChange={(e) => setDirection(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="shopify_to_woocommerce">Shopify → WooCommerce</option>
                        <option value="woocommerce_to_shopify">WooCommerce → Shopify</option>
                    </select>
                </div>

                {/* Mode */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Migration Mode
                    </label>
                    <select
                        value={mode}
                        onChange={(e) => setMode(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="full">Full Migration</option>
                        <option value="incremental">Incremental</option>
                        <option value="test">Test (Preview Only)</option>
                        <option value="batch">Batch</option>
                    </select>
                </div>

                {/* Entities */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Entities to Migrate
                    </label>
                    <div className="space-y-2">
                        {['products', 'customers', 'orders'].map((entity) => (
                            <label key={entity} className="flex items-center">
                                <input
                                    type="checkbox"
                                    checked={entities.includes(entity)}
                                    onChange={() => toggleEntity(entity)}
                                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                                />
                                <span className="ml-2 text-gray-700 capitalize">{entity}</span>
                            </label>
                        ))}
                    </div>
                </div>

                <div className="flex gap-4">
                    <Button type="submit" variant="primary" size="lg" className="flex-1">
                        Start Migration
                    </Button>
                    <Button type="button" variant="secondary" size="lg" onClick={() => navigate('/dashboard')}>
                        Cancel
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default MigrationSetup;
