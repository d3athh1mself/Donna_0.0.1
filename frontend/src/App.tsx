import { useEffect, useState } from 'react'
import './App.css'
import { getHealthStatus } from './api/health'

type BackendHealth = 'checking' | 'ok' | 'unavailable'

function App() {
  const [backendHealth, setBackendHealth] = useState<BackendHealth>('checking')

  useEffect(() => {
    let isCurrent = true

    getHealthStatus()
      .then(() => {
        if (isCurrent) {
          setBackendHealth('ok')
        }
      })
      .catch(() => {
        if (isCurrent) {
          setBackendHealth('unavailable')
        }
      })

    return () => {
      isCurrent = false
    }
  }, [])

  const backendHealthLabel =
    backendHealth === 'ok'
      ? 'Backend ok'
      : backendHealth === 'unavailable'
        ? 'Backend unavailable'
        : 'Backend checking'

  return (
    <main className="app-shell">
      <header className="app-header" aria-label="Donna application header">
        <div>
          <p className="eyebrow">Denali Craft Operations Platform</p>
          <h1>Donna</h1>
        </div>
        <span className={`status-pill status-pill--${backendHealth}`}>
          {backendHealthLabel}
        </span>
      </header>

      <section className="workspace-panel" aria-labelledby="workspace-title">
        <p className="eyebrow">Internal operations</p>
        <h2 id="workspace-title">Ready for the next MVP slice</h2>
        <p>
          This shell is the starting point for Donna's local material catalog,
          supplier records, receipt review, and reporting workflows.
        </p>
      </section>
    </main>
  )
}

export default App
