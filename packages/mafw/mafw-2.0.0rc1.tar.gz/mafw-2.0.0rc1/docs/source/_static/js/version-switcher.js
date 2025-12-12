
// _static/js/version-switcher.js
(async function () {
  // Wait for DOM to be fully loaded
  if (document.readyState === 'loading') {
    await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
  }

  // fetch versions.json from current directory
  let versions = [];
  try {
    const resp = await fetch('versions.json');
    versions = await resp.json();
  } catch (err) {
    console.warn('Could not load versions.json:', err);
    return;
  }

  // Get version from URL by finding the segment that matches a known version
  function getVersionFromPath(versions) {
    const pathSegments = location.pathname.split('/').filter(p => p);

    // Check each segment to see if it matches a known version
    for (const segment of pathSegments) {
      for (const v of versions) {
        if (v.version === segment || v.path === segment) {
          return segment;
        }
      }
    }
    return null;
  }

  // Build URL for a different version, preserving the page path
  function buildVersionUrl(targetVersion, currentVersion) {
    // Replace the current version in the path with target version
    const path = location.pathname;

    // Find and replace the version segment
    const pathSegments = path.split('/');
    const versionIndex = pathSegments.findIndex(seg => seg === currentVersion);

    if (versionIndex !== -1) {
      pathSegments[versionIndex] = targetVersion;
      return pathSegments.join('/');
    }

    // Fallback: couldn't find version in path
    console.warn('Could not find current version in path');
    return path;
  }

  // Now identify the current version
  const currentVersion = getVersionFromPath(versions);

  if (!currentVersion) {
    console.warn('Could not identify current version from path:', location.pathname);
  }

  // find stable mapping
  const stableEntry = versions.find(v => v.version === 'stable') || versions.find(v => v.label === 'stable');
  const stablePath = stableEntry ? stableEntry.path : null;

  // Check if a URL exists
  async function urlExists(url) {
    try {
      const response = await fetch(url, { method: 'HEAD' });
      return response.ok;
    } catch (err) {
      return false;
    }
  }

  // build selector UI
  function createSelector() {
    const sel = document.createElement('select');
    sel.id = 'version-select';
    sel.title = 'Select documentation version';
    versions.forEach(v => {
      // skip alias entries for dropdown; show only real versions + latest
      if (v.label === 'alias') return;
      const opt = document.createElement('option');
      opt.value = v.path;
      opt.textContent = v.version + (v.label ? ` (${v.label})` : '');
      sel.appendChild(opt);
    });

    // set current selection based on actual current version
    if (currentVersion) {
      const currentEntry = versions.find(v => v.path === currentVersion || v.version === currentVersion);
      if (currentEntry) {
        sel.value = currentEntry.path;
      }
    }

    sel.addEventListener('change', async function () {
      const newVersion = this.value;

      if (!currentVersion) {
        console.error('Cannot switch versions: current version not identified');
        return;
      }

      const newPath = buildVersionUrl(newVersion, currentVersion);

      // Check if the page exists in the new version
      const exists = await urlExists(newPath);

      if (exists) {
        // Page exists, redirect to it
        location.href = newPath;
      } else {
        // Page doesn't exist, redirect to version index
        const pathParts = location.pathname.split('/');
        const versionIndex = pathParts.findIndex(seg => seg === currentVersion);
        if (versionIndex !== -1) {
          pathParts[versionIndex] = newVersion;
          // Keep only base path + version, then add index.html
          const baseParts = pathParts.slice(0, versionIndex + 2);
          const indexPath = baseParts.join('/') + (baseParts[baseParts.length - 1] ? '/index.html' : 'index.html');
          console.warn(`Page not found in ${newVersion}, redirecting to index`);
          location.href = indexPath;
        }
      }
    });

    return sel;
  }

  // Wait for element to appear (handles dynamic loading)
  function waitForElement(selector, timeout = 5000) {
    return new Promise((resolve, reject) => {
      const element = document.querySelector(selector);
      if (element) return resolve(element);

      const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
          observer.disconnect();
          resolve(element);
        }
      });

      observer.observe(document.body, { childList: true, subtree: true });

      setTimeout(() => {
        observer.disconnect();
        reject(new Error(`Element ${selector} not found within ${timeout}ms`));
      }, timeout);
    });
  }

  // attach selector to top nav
  async function attachSelector(sel) {
    try {
      // Wait for the element to be available
      const header = await waitForElement(".rst-versions");

      const container = document.createElement('div');
      container.style.display = 'flex';
      container.style.marginTop = '8px';
      container.style.marginBottom = '8px';
      container.style.marginLeft = 'auto';
      container.style.marginRight = 'auto';
      container.style.paddingRight = '10px';
      container.style.justifyContent = 'center';

      const text = document.createElement('span');
      text.style.paddingRight = '5px';
      text.style.margin = 'auto';
      text.textContent = 'Available versions:';
      container.appendChild(text)
      container.appendChild(sel);
      // insert as first child of header if present
      header.insertBefore(container, header.firstChild);
    } catch (error) {
      console.warn("Element with class '.rst-versions' not found. Selector not attached.", error);
    }
  }

  // create and attach
  const selector = createSelector();
  attachSelector(selector);

  // banner when not on stable: show notice pointing to stable equivalent page
  function showBannerIfNotStable() {
    if (!currentVersion || !stablePath) return;

    // Resolve the actual version (in case current is 'stable' alias pointing to a version)
    const currentEntry = versions.find(v => v.path === currentVersion || v.version === currentVersion);
    const actualCurrentPath = currentEntry ? currentEntry.path : currentVersion;

    // Check if we're on stable
    // - Direct match: currentVersion === 'stable'
    // - Or: current path resolves to the same path as stable
    const isStable = currentVersion === 'stable' || actualCurrentPath === stablePath;

    if (isStable) return; // Don't show banner on stable

    // compute equivalent stable URL
    const stableUrl = buildVersionUrl(stablePath, currentVersion);

    // create banner element
    const banner = document.createElement('div');
    banner.id = 'doc-version-banner';
    banner.style.background = '#fff3cd';
    banner.style.border = '1px solid #ffeeba';
    banner.style.padding = '10px';
    banner.style.textAlign = 'center';
    banner.style.fontSize = '14px';
    banner.style.zIndex = '9999';
    banner.style.margin = '20px';

    if (currentVersion === 'latest') {
        banner.innerHTML = `
          You are viewing the development version of the documentation.
          For the stable version of this page, <a href="${stableUrl}">click here</a>.
        `;
    } else {
        banner.innerHTML = `
          You are viewing an older version of the documentation.
          For the stable version of this page, <a href="${stableUrl}">click here</a>.
        `;
    }

    const navContent = document.querySelector(".wy-nav-content")
    if (navContent) {
        navContent.insertBefore(banner, navContent.firstChild)
    } else {
        document.body.insertBefore(banner, document.body.firstChild);
    }
  }

  showBannerIfNotStable();
})();