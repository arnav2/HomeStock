#!/usr/bin/env node
/**
 * Cross-platform script to build Python backend before Electron packaging
 */
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const platform = os.platform();
const scriptPath = path.join(__dirname, platform === 'win32' ? 'build_backend.bat' : 'build_backend.sh');

console.log(`🔨 Building Python backend for ${platform}...`);

if (!fs.existsSync(scriptPath)) {
  console.error(`❌ Build script not found: ${scriptPath}`);
  process.exit(1);
}

const buildProcess = spawn(scriptPath, [], {
  stdio: 'inherit',
  shell: true,
  cwd: path.join(__dirname, '..')
});

buildProcess.on('close', (code) => {
  if (code !== 0) {
    console.error(`❌ Backend build failed with code ${code}`);
    process.exit(code);
  }
  console.log('✅ Backend build complete!');
});

buildProcess.on('error', (error) => {
  console.error(`❌ Failed to start build process: ${error.message}`);
  process.exit(1);
});

