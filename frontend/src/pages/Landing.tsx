import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE, setApiKey } from '../App'

export default function Landing() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [key, setKey] = useState('')
  const navigate = useNavigate()

  const handleSignup = async () => {
    if (!email) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })
      const data = await res.json()
      setApiKey(data.api_key)
      setKey(data.api_key)
    } catch (e) {
      alert('Server not running. Start the backend first.')
    }
    setLoading(false)
  }

  const handleGo = () => {
    if (key) navigate('/dashboard')
  }

  return (
    <div style={{ maxWidth: 700, margin: '80px auto', padding: 24, textAlign: 'center' }}>
      <h1 style={{ fontSize: 48, fontWeight: 800, background: 'linear-gradient(135deg, #7c5cfc, #b35cfc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: 16 }}>
        Synthara
      </h1>
      <p style={{ fontSize: 20, color: '#888', marginBottom: 40 }}>
        Describe an AI agent. We build it. You deploy it.
      </p>

      {!key ? (
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{ padding: '14px 20px', borderRadius: 8, border: '1px solid #2a2a4e', background: '#12121f', color: '#fff', fontSize: 16, width: 280 }}
          />
          <button
            onClick={handleSignup}
            disabled={loading}
            style={{ padding: '14px 28px', borderRadius: 8, border: 'none', background: '#7c5cfc', color: '#fff', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}
          >
            {loading ? '...' : 'Get API Key'}
          </button>
        </div>
      ) : (
        <div style={{ background: '#12121f', border: '1px solid #2a2a4e', borderRadius: 12, padding: 24 }}>
          <p style={{ color: '#4ade80', marginBottom: 8 }}>Your API Key (save this):</p>
          <code style={{ background: '#1a1a2e', padding: '12px 20px', borderRadius: 8, display: 'block', wordBreak: 'break-all', fontSize: 14, marginBottom: 16 }}>
            {key}
          </code>
          <button
            onClick={handleGo}
            style={{ padding: '14px 28px', borderRadius: 8, border: 'none', background: '#7c5cfc', color: '#fff', fontSize: 16, fontWeight: 600, cursor: 'pointer' }}
          >
            Go to Dashboard →
          </button>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginTop: 60 }}>
        {[
          { title: '1. Describe', desc: 'Tell us what your agent should do in plain English' },
          { title: '2. AI Generates', desc: 'Our AI creates the perfect system prompt and configuration' },
          { title: '3. Deploy & Chat', desc: 'Your agent is ready in seconds — chat with it immediately' },
        ].map(f => (
          <div key={f.title} style={{ background: '#12121f', border: '1px solid #1a1a2e', borderRadius: 12, padding: 24 }}>
            <h3 style={{ color: '#7c5cfc', marginBottom: 8 }}>{f.title}</h3>
            <p style={{ color: '#888', fontSize: 14 }}>{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
