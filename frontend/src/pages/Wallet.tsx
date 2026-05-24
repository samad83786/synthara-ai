import { useEffect, useState } from 'react'
import { API_BASE, getApiKey } from '../App'

export default function Wallet() {
  const [credits, setCredits] = useState(0)
  const [wallet, setWallet] = useState('')
  const [amount, setAmount] = useState(0.5)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/credits`, {
      headers: { 'x-api-key': getApiKey() || '' },
    }).then(r => r.json()).then(d => setCredits(d.credits))

    fetch(`${API_BASE}/wallet`).then(r => r.json()).then(d => setWallet(d.wallet))
  }, [])

  const handleCopy = () => {
    if (wallet) {
      navigator.clipboard.writeText(wallet)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', padding: 24 }}>
      <h2 style={{ marginBottom: 24 }}>Wallet</h2>

      <div style={{ background: '#12121f', border: '1px solid #2a2a4e', borderRadius: 12, padding: 24, marginBottom: 20 }}>
        <p style={{ color: '#888', fontSize: 14, marginBottom: 4 }}>Your Balance</p>
        <p style={{ fontSize: 36, fontWeight: 700, color: '#4ade80' }}>{credits.toFixed(2)}</p>
        <p style={{ color: '#666', fontSize: 12 }}>credits (1 credit ≈ 1 API call)</p>
      </div>

      <div style={{ background: '#12121f', border: '1px solid #2a2a4e', borderRadius: 12, padding: 24 }}>
        <h3 style={{ marginBottom: 16, fontSize: 16 }}>Top Up with Solana</h3>

        <p style={{ color: '#888', fontSize: 13, marginBottom: 12 }}>
          Send SOL to the wallet below. Credits are added automatically.
        </p>

        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <input
            type="number"
            value={amount}
            onChange={e => setAmount(parseFloat(e.target.value) || 0)}
            step={0.1}
            min={0.1}
            style={{ width: 100, padding: '10px 12px', borderRadius: 8, border: '1px solid #2a2a4e', background: '#0a0a0f', color: '#fff', fontSize: 16 }}
          />
          <span style={{ color: '#888', alignSelf: 'center' }}>SOL</span>
        </div>

        {wallet ? (
          <div>
            <p style={{ color: '#888', fontSize: 13, marginBottom: 8 }}>Send to this address:</p>
            <div
              onClick={handleCopy}
              style={{ background: '#0a0a0f', border: '1px solid #2a2a4e', borderRadius: 8, padding: '12px 16px', cursor: 'pointer', wordBreak: 'break-all', fontFamily: 'monospace', fontSize: 13, color: '#7c5cfc' }}
            >
              {wallet}
            </div>
            <p style={{ color: copied ? '#4ade80' : '#666', fontSize: 12, marginTop: 8 }}>
              {copied ? 'Copied!' : 'Click to copy address'}
            </p>
          </div>
        ) : (
          <div style={{ background: '#1a1a2e', borderRadius: 8, padding: 16, textAlign: 'center' }}>
            <p style={{ color: '#f59e0b', fontSize: 14, marginBottom: 8 }}>No wallet configured yet</p>
            <p style={{ color: '#666', fontSize: 12 }}>Set SYNTHARA_WALLET env var to enable crypto payments</p>
          </div>
        )}

        <div style={{ marginTop: 20, padding: 12, background: '#1a1a2e', borderRadius: 8 }}>
          <p style={{ color: '#888', fontSize: 12 }}>
            <strong style={{ color: '#f59e0b' }}>Note:</strong> Credits are added once the transaction is confirmed on-chain. This usually takes a few seconds.
          </p>
        </div>
      </div>
    </div>
  )
}
