import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE, getApiKey } from '../App'

export default function Dashboard() {
  const [agents, setAgents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch(`${API_BASE}/agents`, {
      headers: { 'x-api-key': getApiKey() || '' },
    })
      .then(r => r.json())
      .then(d => setAgents(d.agents || []))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div style={{ padding: 40, textAlign: 'center', color: '#888' }}>Loading...</div>

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>Your Agents</h2>
        <button
          onClick={() => navigate('/create')}
          style={{ padding: '10px 20px', borderRadius: 8, border: 'none', background: '#7c5cfc', color: '#fff', fontSize: 14, fontWeight: 600, cursor: 'pointer' }}
        >
          + New Agent
        </button>
      </div>

      {agents.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 60, color: '#666' }}>
          <p style={{ fontSize: 18, marginBottom: 8 }}>No agents yet</p>
          <p style={{ fontSize: 14 }}>Create your first agent to get started</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {agents.map(a => (
            <div
              key={a.id}
              onClick={() => navigate(`/chat/${a.id}`)}
              style={{ background: '#12121f', border: '1px solid #1a1a2e', borderRadius: 12, padding: '16px 20px', cursor: 'pointer', transition: 'border-color 0.2s' }}
              onMouseEnter={e => e.currentTarget.style.borderColor = '#7c5cfc'}
              onMouseLeave={e => e.currentTarget.style.borderColor = '#1a1a2e'}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: 0, color: '#7c5cfc' }}>{a.name}</h3>
                  <p style={{ margin: '4px 0 0', color: '#666', fontSize: 13 }}>{a.description}</p>
                </div>
                <span style={{ fontSize: 12, color: '#444', background: '#0a0a0f', padding: '4px 8px', borderRadius: 4 }}>{a.model}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
