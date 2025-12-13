document.addEventListener('DOMContentLoaded', function() {
  const serverStatusElement = document.getElementById('serverStatus');
  const showPasswordCheckbox = document.getElementById('showPasswordValues');

  const SERVER_URL = 'http://localhost:3001';

  // Function to format uptime in human readable format
  function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
      return `${minutes}m`;
    } else {
      return `${Math.floor(seconds)}s`;
    }
  }

  // Function to check server connectivity and get detailed status
  async function checkServerStatus() {
    const serverDetailsElement = document.getElementById('serverDetails');
    const installationPathElement = document.getElementById('installationPath');
    const serverUptimeElement = document.getElementById('serverUptime');

    try {
      const response = await fetch(`${SERVER_URL}/status`, { 
        method: 'GET',
        signal: AbortSignal.timeout(5000) // 5 second timeout
      });
      
      if (response.ok) {
        const statusData = await response.json();
        
        // Server is connected - show success status
        serverStatusElement.textContent = `http://localhost:3001 Connected`;
        serverStatusElement.style.color = '#4CAF50';
        
        // Show detailed information
        installationPathElement.textContent = statusData.installationPath || 'Unknown';
        serverUptimeElement.textContent = statusData.uptime ? formatUptime(statusData.uptime) : 'Unknown';
        serverDetailsElement.style.display = 'block';
        
      } else {
        throw new Error(`Server returned ${response.status}`);
      }
    } catch (error) {
      // Server is not responding - show error status
      serverStatusElement.textContent = `http://localhost:3001 Not running`;
      serverStatusElement.style.color = '#f44336';
      
      // Hide detailed information
      serverDetailsElement.style.display = 'none';
    }
  }

  // Load and save password visibility setting
  async function loadSettings() {
    try {
      const result = await chrome.storage.local.get(['showPasswordValues']);
      showPasswordCheckbox.checked = result.showPasswordValues || false;
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }

  async function savePasswordSetting() {
    try {
      await chrome.storage.local.set({ showPasswordValues: showPasswordCheckbox.checked });
      // Notify content scripts of the change
      chrome.tabs.query({}, (tabs) => {
        tabs.forEach(tab => {
          chrome.tabs.sendMessage(tab.id, {
            type: 'settingChanged',
            setting: 'showPasswordValues', 
            value: showPasswordCheckbox.checked
          }).catch(() => {}); // Ignore errors for tabs without content script
        });
      });
      console.log(`Password visibility: ${showPasswordCheckbox.checked ? 'Enabled' : 'Disabled'}`);
    } catch (error) {
      console.error('Error saving setting:', error);
    }
  }

  // Event listeners
  showPasswordCheckbox.addEventListener('change', savePasswordSetting);

  // Load settings and initial server check
  loadSettings();
  checkServerStatus();

  // Check server status every 10 seconds
  setInterval(checkServerStatus, 10000);
}); 