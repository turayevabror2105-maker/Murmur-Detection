import https from 'https';

const url = 'https://registry.npmjs.org/';

const req = https.get(url, { timeout: 5000 }, (res) => {
  if (res.statusCode && res.statusCode >= 200 && res.statusCode < 400) {
    console.log('npm registry connectivity: ok');
    process.exit(0);
  }
  console.warn(`npm registry returned status ${res.statusCode}.`);
  console.warn('If you see 403 errors, run:');
  console.warn('  npm config set registry https://registry.npmjs.org/');
  console.warn('  npm config delete proxy');
  console.warn('  npm config delete https-proxy');
  console.warn('  npm config set strict-ssl true');
  console.warn('If on a restricted network, use Docker-only workflow or VPN.');
  process.exit(0);
});

req.on('error', () => {
  console.warn('npm registry connectivity check failed.');
  console.warn('If you see 403 errors, run:');
  console.warn('  npm config set registry https://registry.npmjs.org/');
  console.warn('  npm config delete proxy');
  console.warn('  npm config delete https-proxy');
  console.warn('  npm config set strict-ssl true');
  console.warn('If on a restricted network, use Docker-only workflow or VPN.');
  process.exit(0);
});

req.on('timeout', () => {
  console.warn('npm registry connectivity timed out.');
  req.destroy();
  process.exit(0);
});
