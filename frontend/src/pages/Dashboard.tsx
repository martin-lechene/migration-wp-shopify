/**
 * Dashboard page
 */
import React, { useEffect } from 'react';
import { Activity, Database, Users, ShoppingCart } from 'lucide-react';
import { useMigrationStore } from '@/store/migrationStore';
import Loading from '@/components/common/Loading';

export const Dashboard: React.FC = () => {
    const { jobs, fetchJobs, isLoading } = useMigrationStore();

    useEffect(() => {
        fetchJobs();
    }, [fetchJobs]);

    const stats = [
        { name: 'Total Migrations', value: jobs.length, icon: Activity, color: 'bg-blue-500' },
        { name: 'Products Migrated', value: jobs.reduce((sum, j) => sum + j.migrated_items, 0), icon: Database, color: 'bg-green-500' },
        { name: 'In Progress', value: jobs.filter(j => j.status === 'in_progress').length, icon: Users, color: 'bg-yellow-500' },
        { name: 'Completed', value: jobs.filter(j => j.status === 'completed').length, icon: ShoppingCart, color: 'bg-purple-500' },
    ];

    if (isLoading) {
        return <Loading text="Loading dashboard..." />;
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                <p className="text-gray-600">Overview of your migration activities</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat) => (
                    <div key={stat.name} className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600">{stat.name}</p>
                                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                            </div>
                            <div className={`p-3 rounded-lg ${stat.color}`}>
                                <stat.icon className="w-6 h-6 text-white" />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Recent Migrations */}
            <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b">
                    <h2 className="text-xl font-semibold text-gray-900">Recent Migrations</h2>
                </div>
                <div className="p-6">
                    {jobs.length === 0 ? (
                        <p className="text-gray-500 text-center py-8">No migrations yet. Start your first migration!</p>
                    ) : (
                        <div className="space-y-4">
                            {jobs.slice(0, 5).map((job) => (
                                <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                                    <div>
                                        <p className="font-medium text-gray-900">{job.direction}</p>
                                        <p className="text-sm text-gray-500">
                                            {job.migrated_items} / {job.total_items} items migrated
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${job.status === 'completed' ? 'bg-green-100 text-green-800' :
                                                job.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                                                    job.status === 'failed' ? 'bg-red-100 text-red-800' :
                                                        'bg-gray-100 text-gray-800'
                                            }`}>
                                            {job.status}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
