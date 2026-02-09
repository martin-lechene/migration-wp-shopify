/**
 * Main layout with sidebar and header
 */
import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { Home, Database, Users, ShoppingCart, Settings, BarChart, FileText, LogOut } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

export const MainLayout: React.FC = () => {
    const { user, logout } = useAuthStore();

    const navigation = [
        { name: 'Dashboard', href: '/dashboard', icon: Home },
        { name: 'Products', href: '/migration/products', icon: Database },
        { name: 'Customers', href: '/migration/customers', icon: Users },
        { name: 'Orders', href: '/migration/orders', icon: ShoppingCart },
        { name: 'Monitoring', href: '/monitoring', icon: BarChart },
        { name: 'Reports', href: '/reports', icon: FileText },
        { name: 'Settings', href: '/settings', icon: Settings },
    ];

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-lg">
                <div className="flex flex-col h-full">
                    <div className="flex items-center justify-center h-16 bg-blue-600 text-white">
                        <h1 className="text-xl font-bold">Migrator</h1>
                    </div>

                    <nav className="flex-1 px-4 py-4 space-y-2">
                        {navigation.map((item) => (
                            <Link
                                key={item.name}
                                to={item.href}
                                className="flex items-center px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors"
                            >
                                <item.icon className="w-5 h-5 mr-3" />
                                {item.name}
                            </Link>
                        ))}
                    </nav>

                    <div className="p-4 border-t">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-900">{user?.username || 'User'}</p>
                                <p className="text-xs text-gray-500">{user?.email || ''}</p>
                            </div>
                            <button
                                onClick={logout}
                                className="p-2 text-gray-500 hover:text-red-600 rounded-lg hover:bg-gray-100"
                                title="Logout"
                            >
                                <LogOut className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <header className="bg-white shadow-sm h-16 flex items-center px-6">
                    <h2 className="text-2xl font-semibold text-gray-800">Migration Dashboard</h2>
                </header>

                {/* Page content */}
                <main className="flex-1 overflow-y-auto p-6">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default MainLayout;
