import { useEffect, useState } from 'react'
import { API_BASE } from '../App'

export default function Admin() {
  const [adminKey, setAdminKey] = useState('')
  const [authed, setAuthed] = useState(false)
  const [tab, setTab] = useState('stats')
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    const saved = localStorage.getItem('synthara_admin_key')
    if (saved) { setAdminKey(saved); setAuthed(true) }
  }, [])

  async function login() {
    localStorage.setItem('synthara_admin_key', adminKey)
    setAuthed(true)
  }

  async function fetchData(endpoint: string) {
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        headers: { 'x-api-key': adminKey }
      })
      const d = await res.json()
      setData(d)
    } catch (e: any) {
      setData({ error: e.message })
    }
  }

  useEffect(() => {
    if (authed) fetchData('/admin/stats')
  }, [authed])

  if (!authed) {
    return (
      <div style={{ padding: 40, maxWidth: 400, margin: '0 auto' }}>
        <h2>Admin Login</h2>
        <input
          type="password"
          placeholder="Admin API Key"
          value={adminKey}
          onChange={e => setAdminKey(e.target.value)}
          style={{ width: '100%', padding: 10, margin: '10px 0', borderRadius: 6, border: '1px solid #333', background: '#1a1a2e', color: '#e0e0e0' }}
        />
        <button onClick={login} style={{ padding: '10px 24px', background: '#7c5cfc', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer' }}>Login</button>
      </div>
    )
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: '0 auto' }}>
      <h2 style={{ color: '#7c5cfc' }}>Admin Dashboard</h2>
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {['stats','users','agents','usage','payments'].map(t => (
          <button
            key={t}
            onClick={() => { setTab(t); fetchData(`/admin/${t}`) }}
            style={{
              padding: '8px 16px', background: tab === t ? '#7c5cfc' : '#1a1a2e',
              border: '1px solid #333', borderRadius: 6, color: '#e0e0e0', cursor: 'pointer', textTransform: 'capitalize'
            }}
          >{t}</button>
        ))}
      </div>
      {data && <div style={{ background: '#1a1a2e', borderRadius: 8, padding: 20, overflow: 'auto' }}>
        <pre style={{ fontSize: 13, lineHeight: 1.6 }}>{JSON.stringify(data, null, 2)}</pre>
      </div>}
    </div>
  )
}