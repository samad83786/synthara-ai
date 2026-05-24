import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE, getApiKey } from '../App'

export default function CreateAgent() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const navigate = useNavigate()

  const handleCreate = async () => {
    if (!name || !description) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/agents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': getApiKey() || '',
        },
        body: JSON.stringify({ name, description }),
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      alert('Error creating agent')
    }
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', padding: 24 }}>
      <h2 style={{ marginBottom: 24 }}>Create an AI Agent</h2>

      <label style={{ display: 'block', marginBottom: 6, color: '#888', fontSize: 14 }}>Agent Name</label>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="e.g., ResearchBot"
        style={{ width: '100%', padding: '12px 16px', borderRadius: 8, border: '1px solid #2a2a4e', background: '#12121f', color: '#fff', fontSize: 16, marginBottom: 20, boxSizing: 'border-box' }}
      />

      <label style={{ display: 'block', marginBottom: 6, color: '#888', fontSize: 14 }}>What should this agent do?</label>
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="e.g., Research any topic deeply by searching the web, analyzing content, and generating comprehensive reports with citations"
        rows={5}
        style={{ width: '100%', padding: '12px 16px', borderRadius: 8, border: '1px solid #2a2a4e', background: '#12121f', color: '#fff', fontSize: 16, fontFamily: 'inherit', resize: 'vertical', marginBottom: 20, boxSizing: 'border-box' }}
      />

      <button
        onClick={handleCreate}
        disabled={loading || !name || !description}
        style={{ padding: '14px 28px', borderRadius: 8, border: 'none', background: loading ? '#555' : '#7c5cfc', color: '#fff', fontSize: 16, fontWeight: 600, cursor: loading ? 'default' : 'pointer', width: '100%' }}
      >
        {loading ? 'Generating Agent...' : 'Create Agent with AI →'}
      </button>

      {result && (
        <div style={{ marginTop: 24, background: '#12121f', border: '1px solid #2a2a4e', borderRadius: 12, padding: 20 }}>
          <p style={{ color: '#4ade80', marginBottom: 8 }}>Agent Created!</p>
          <p style={{ color: '#7c5cfc', fontWeight: 600 }}>{result.name}</p>
          <p style={{ color: '#888', fontSize: 13, marginTop: 8, marginBottom: 12 }}>System Prompt:</p>
          <code style={{ fontSize: 12, color: '#aaa', lineHeight: 1.6, display: 'block', whiteSpace: 'pre-wrap', background: '#0a0a0f', padding: 12, borderRadius: 8, maxHeight: 200, overflowY: 'auto' }}>
            {result.system_prompt}
          </code>
          <button
            onClick={() => navigate('/dashboard')}
            style={{ marginTop: 16, padding: '10px 20px', borderRadius: 8, border: '1px solid #7c5cfc', background: 'transparent', color: '#7c5cfc', cursor: 'pointer' }}
          >
            View All Agents →
          </button>
        </div>
      )}
    </div>
  )
}
