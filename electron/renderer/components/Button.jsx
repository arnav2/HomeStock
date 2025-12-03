import React from 'react';

const Button = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  disabled = false,
  small = false,
  className = '',
  ...props 
}) => {
  const baseClasses = small 
    ? 'px-3 py-1.5 text-sm rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
    : 'px-5 py-2.5 rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variantClasses = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600',
    secondary: 'bg-gray-500 text-white hover:bg-gray-600',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${className}`;

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={classes}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;

