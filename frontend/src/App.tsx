import './App.css'

function App() {
  return (
    <main className="app-shell">
      <header className="app-header" aria-label="Donna application header">
        <div>
          <p className="eyebrow">Denali Craft Operations Platform</p>
          <h1>Donna</h1>
        </div>
        <span className="status-pill">Frontend setup</span>
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
