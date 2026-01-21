import { readFileSync } from 'fs'

const app = readFileSync('./src/App.tsx', 'utf-8')
if (!app.includes('Upload')) {
  throw new Error('Smoke test failed: Upload page not found')
}
console.log('Smoke test passed')
