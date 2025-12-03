import React from 'react';

const StatusMessage = ({ message, type = 'info', className = '' }) => {
  if (!message) return null;

  const typeClasses = {
    success: 'bg-green-100 border-green-400 text-green-700',
    error: 'bg-red-100 border-red-400 text-red-700',
    info: 'bg-blue-100 border-blue-400 text-blue-700',
  };

  // Check if message contains HTML
  const containsHTML = /<[a-z][\s\S]*>/i.test(message);

  return (
    <div 
      className={`mt-4 p-3 rounded border ${typeClasses[type]} ${className}`}
      dangerouslySetInnerHTML={containsHTML ? { __html: message } : undefined}
    >
      {!containsHTML && message}
    </div>
  );
};

export default StatusMessage;

