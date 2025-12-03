import React from 'react';

const StatusCard = ({ title, value }) => {
  return (
    <div className="bg-white p-5 rounded-lg shadow-sm">
      <h3 className="text-sm text-gray-500 uppercase tracking-wide mb-2">{title}</h3>
      <p className="text-3xl font-semibold text-gray-800">{value}</p>
    </div>
  );
};

export default StatusCard;

