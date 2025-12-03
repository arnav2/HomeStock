#!/usr/bin/env node
/**
 * Check if all prerequisites are met for building the application
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

let errors = [];
let warnings = [];

console.log('🔍 Checking build prerequisites...\n');

// Check Python
try {
  const pythonVersion = execSync('python3 --version', { encoding: 'utf-8' }).trim();
  console.log(`✅ Python: ${pythonVersion}`);
  
  // Check version (should be 3.10+)
  const versionMatch = pythonVersion.match(/Python (\d+)\.(\d+)/);
  if (versionMatch) {
    const major = parseInt(versionMatch[1]);
    const minor = parseInt(versionMatch[2]);
    if (major < 3 || (major === 3 && minor < 10)) {
      errors.push(`Python 3.10+ required, found ${major}.${minor}`);
    }
  }
} catch (e) {
  errors.push('Python 3 not found. Please install Python 3.10+');
}

// Check Node.js
try {
  const nodeVersion = execSync('node --version', { encoding: 'utf-8' }).trim();
  console.log(`✅ Node.js: ${nodeVersion}`);
  
  // Check version (should be 20+)
  const versionMatch = nodeVersion.match(/v(\d+)/);
  if (versionMatch) {
    const major = parseInt(versionMatch[1]);
    if (major < 20) {
      warnings.push(`Node.js 20+ recommended, found ${major}`);
    }
  }
} catch (e) {
  errors.push('Node.js not found. Please install Node.js 20+');
}

// Check npm
try {
  const npmVersion = execSync('npm --version', { encoding: 'utf-8' }).trim();
  console.log(`✅ npm: ${npmVersion}`);
} catch (e) {
  errors.push('npm not found');
}

// Check if backend venv exists
const venvPath = path.join(__dirname, '..', 'backend', 'venv');
if (!fs.existsSync(venvPath)) {
  warnings.push('Backend virtual environment not found. Run setup script first.');
} else {
  console.log('✅ Backend virtual environment found');
}

// Check if node_modules exists
const nodeModulesPath = path.join(__dirname, '..', 'node_modules');
if (!fs.existsSync(nodeModulesPath)) {
  warnings.push('Node modules not found. Run "npm install" first.');
} else {
  console.log('✅ Node modules found');
}

// Check PyInstaller
try {
  const pyinstallerPath = path.join(venvPath, process.platform === 'win32' ? 'Scripts' : 'bin', 'pyinstaller');
  if (fs.existsSync(pyinstallerPath) || fs.existsSync(pyinstallerPath + '.exe')) {
    console.log('✅ PyInstaller found');
  } else {
    warnings.push('PyInstaller not found in venv. Will be installed during build.');
  }
} catch (e) {
  warnings.push('Could not check PyInstaller');
}

// Check electron-builder
try {
  const electronBuilderPath = path.join(nodeModulesPath, '.bin', 'electron-builder');
  if (fs.existsSync(electronBuilderPath) || fs.existsSync(electronBuilderPath + '.cmd')) {
    console.log('✅ electron-builder found');
  } else {
    warnings.push('electron-builder not found. Run "npm install" first.');
  }
} catch (e) {
  warnings.push('Could not check electron-builder');
}

// Platform-specific checks
const platform = process.platform;
if (platform === 'darwin') {
  try {
    execSync('xcode-select -p', { stdio: 'ignore' });
    console.log('✅ Xcode Command Line Tools found');
  } catch (e) {
    warnings.push('Xcode Command Line Tools not found. Install with: xcode-select --install');
  }
} else if (platform === 'win32') {
  console.log('ℹ️  Windows: Ensure Visual Studio Build Tools are installed');
}

console.log('\n');

if (errors.length > 0) {
  console.error('❌ Errors found:');
  errors.forEach(err => console.error(`   - ${err}`));
  console.error('\nPlease fix these errors before building.');
  process.exit(1);
}

if (warnings.length > 0) {
  console.warn('⚠️  Warnings:');
  warnings.forEach(warn => console.warn(`   - ${warn}`));
  console.warn('\nThese may cause issues during build.');
}

if (errors.length === 0 && warnings.length === 0) {
  console.log('✅ All prerequisites met! Ready to build.');
}

