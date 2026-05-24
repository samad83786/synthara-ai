import { useEffect, useState, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { API_BASE, getApiKey } from '../App'

export default function Chat() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [agent, setAgent] = useState<any>(null)
  const [messages, setMessages] = useState<{role: string, content: string}[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [credits, setCredits] = useState(0)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetch(`${API_BASE}/agents`, {
      headers: { 'x-api-key': getApiKey() || '' },
    })
      .then(r => r.json())
      .then(d => {
        const a = (d.agents || []).find((x: any) => x.id === Number(id))
        if (a) setAgent(a)
        else navigate('/dashboard')
      })
    fetch(`${API_BASE}/credits`, {
      headers: { 'x-api-key': getApiKey() || '' },
    })
      .then(r => r.json())
      .then(d => setCredits(d.credits))
  }, [id])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || sending) return
    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setSending(true)

    try {
      const res = await fetch(`${API_BASE}/agents/${id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': getApiKey() || '',
        },
        body: JSON.stringify({ message: input }),
      })
      const data = await res.json()
      if (res.status === 402) {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Insufficient credits. Please top up in Wallet.' }])
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
      }
      const creditsRes = await fetch(`${API_BASE}/credits`, {
        headers: { 'x-api-key': getApiKey() || '' },
      })
      const creditsData = await creditsRes.json()
      setCredits(creditsData.credits)
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to server.' }])
    }
    setSending(false)
  }

  if (!agent) return <div style={{ padding: 40, textAlign: 'center', color: '#888' }}>Loading...</div>

  return (
    <div style={{ maxWidth: 700, margin: '0 auto', padding: 24, display: 'flex', flexDirection: 'column', height: 'calc(100vh - 80px)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0, color: '#7c5cfc' }}>{agent.name}</h2>
          <p style={{ margin: '4px 0 0', color: '#666', fontSize: 13 }}>Credits: {credits.toFixed(2)}</p>
        </div>
        <button onClick={() => navigate('/wallet')} style={{ padding: '8px 16px', borderRadius: 8, border: '1px solid #f59e0b', background: 'transparent', color: '#f59e0b', cursor: 'pointer', fontSize: 13 }}>
          Top Up
        </button>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', background: '#0a0a0f', borderRadius: 12, padding: 16, marginBottom: 16, border: '1px solid #1a1a2e' }}>
        {messages.length === 0 && (
          <p style={{ color: '#555', textAlign: 'center', marginTop: 40 }}>Send a message to start chatting with {agent.name}</p>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 16, textAlign: m.role === 'user' ? 'right' : 'left' }}>
            <div style={{
              display: 'inline-block',
              maxWidth: '80%',
              padding: '12px 16px',
              borderRadius: 12,
              background: m.role === 'user' ? '#7c5cfc' : '#1a1a2e',
              color: '#e0e0e0',
              fontSize: 14,
              lineHeight: 1.5,
              whiteSpace: 'pre-wrap',
            }}>
              {m.content}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="Message your agent..."
          style={{ flex: 1, padding: '12px 16px', borderRadius: 8, border: '1px solid #2a2a4e', background: '#12121f', color: '#fff', fontSize: 16, outline: 'none' }}
        />
        <button
          onClick={handleSend}
          disabled={sending}
          style={{ padding: '12px 24px', borderRadius: 8, border: 'none', background: sending ? '#555' : '#7c5cfc', color: '#fff', fontSize: 16, cursor: sending ? 'default' : 'pointer' }}
        >
          {sending ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
