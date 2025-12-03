# Frontend Architecture

HomeStock uses React with Tailwind CSS for the Electron frontend.

## Project Structure

```
electron/renderer/
├── main.jsx              # React entry point
├── App.jsx               # Main app component with routing
├── index.html            # HTML template
├── index.css             # Global styles with Tailwind imports
├── components/          # Reusable components
│   ├── Sidebar.jsx
│   ├── StatusCard.jsx
│   ├── Button.jsx
│   ├── FormInput.jsx
│   └── StatusMessage.jsx
├── pages/               # Page components
│   ├── Dashboard.jsx
│   ├── Downloads.jsx
│   ├── Parser.jsx
│   ├── Settings.jsx
│   └── Logs.jsx
└── services/            # API service layer
    └── api.js
```

## Key Features

1. **React Router**: Uses HashRouter for Electron compatibility
2. **Component-based Architecture**: All UI elements are reusable components
3. **API Service Layer**: Centralized API calls in `services/api.js`
4. **Tailwind CSS**: Modern utility-first CSS framework
5. **Responsive Design**: Mobile-friendly layouts

## Development

### Running in Development Mode

```bash
npm run dev
```

This will:
1. Start Vite dev server on `http://localhost:5173`
2. Start Electron and load the React app from the dev server
3. Open DevTools automatically

### Building for Production

```bash
npm run build:react    # Build React app
npm run build          # Build React + Backend + Electron app
```

## Routing

All routes are defined in `App.jsx`:
- `/` → Redirects to `/dashboard`
- `/dashboard` → Dashboard page
- `/downloads` → Downloads page
- `/parser` → Parser page
- `/settings` → Settings page
- `/logs` → Logs page

## API Integration

All backend API calls are handled through the `services/api.js` module:
- `dashboardAPI` - Dashboard operations
- `downloadsAPI` - File download operations
- `parserAPI` - File parsing operations
- `settingsAPI` - Settings management
- `logsAPI` - Log viewing

## Styling

- Uses Tailwind CSS utility classes
- Custom colors defined in `tailwind.config.js`
- Responsive design with Tailwind breakpoints
- Consistent component styling throughout

## Components

### Reusable Components

- **Sidebar**: Navigation sidebar with active route highlighting
- **StatusCard**: Card component for displaying statistics
- **Button**: Reusable button with variants (primary, secondary) and size options
- **FormInput**: Form input with label and styling
- **StatusMessage**: Status messages with different types (success, error, info)

### Pages

Each page is a self-contained component that:
- Manages its own state
- Calls appropriate API services
- Handles user interactions
- Displays status messages

## Migration Notes

- Old files (`app.js`, `styles.css`) have been removed
- All functionality from the original HTML/CSS/JS app has been preserved
- Electron IPC communication remains the same through `window.electronAPI`
- Backend API endpoints remain unchanged

