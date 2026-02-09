/**
 * Loading spinner component
 */
import React from 'react';

interface LoadingProps {
    size?: 'sm' | 'md' | 'lg';
    text?: string;
}

export const Loading: React.FC<LoadingProps> = ({ size = 'md', text }) => {
    const sizeStyles = {
        sm: 'h-8 w-8',
        md: 'h-12 w-12',
        lg: 'h-16 w-16',
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[200px]">
            <div className={`animate-spin rounded-full border-4 border-gray-200 border-t-blue-600 ${sizeStyles[size]}`} />
            {text && <p className="mt-4 text-gray-600">{text}</p>}
        </div>
    );
};

export default Loading;
