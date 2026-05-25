import { Routes, Route, Link } from 'react-router-dom'
import Landing from './pages/Landing'
import CreateAgent from './pages/CreateAgent'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Wallet from './pages/Wallet'
import Admin from './pages/Admin'

const API_BASE = '/api/v1'

function getApiKey(): string | null {
  return localStorage.getItem('synthara_api_key')
}

function setApiKey(key: string) {
  localStorage.setItem('synthara_api_key', key)
}

export { API_BASE, getApiKey, setApiKey }

export default function App() {
  const apiKey = getApiKey()
  return (
    <div style={{ minHeight: '100vh', background: '#0a0a0f', color: '#e0e0e0', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <nav style={{ padding: '16px 24px', borderBottom: '1px solid #1a1a2e', display: 'flex', alignItems: 'center', gap: 24 }}>
        <Link to="/" style={{ color: '#7c5cfc', fontWeight: 700, fontSize: 20, textDecoration: 'none' }}>Synthara</Link>
        {apiKey && (
          <>
            <Link to="/dashboard" style={{ color: '#999', textDecoration: 'none' }}>Dashboard</Link>
            <Link to="/create" style={{ color: '#999', textDecoration: 'none' }}>Create Agent</Link>
            <Link to="/wallet" style={{ color: '#999', textDecoration: 'none' }}>Wallet</Link>
          </>
        )}
        <Link to="/admin" style={{ color: '#555', textDecoration: 'none', fontSize: 13, marginLeft: 'auto' }}>Admin</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/create" element={<CreateAgent />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chat/:id" element={<Chat />} />
        <Route path="/wallet" element={<Wallet />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </div>
  )
}
