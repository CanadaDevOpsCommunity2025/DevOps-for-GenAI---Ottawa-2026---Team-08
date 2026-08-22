// Trace list + waterfall + span detail, wired together across Tasks 8-10 of
// docs/plans/obeverfy-implementation-plan.md.

import { useState } from 'react';
import { TraceList } from './components/TraceList';
import { supabaseConfiguration } from './supabaseClient';

function ConfigurationError({ issues }) {
  return (
    <main className="setup-state" aria-labelledby="configuration-error-title">
      <section className="setup-panel" role="alert">
        <p className="setup-product">Obeverfy</p>
        <h1 id="configuration-error-title">Dashboard setup required</h1>
        <p>
          Update <code>dashboard/.env</code> and restart the Vite development server.
        </p>
        <ul>
          {issues.map((issue) => (
            <li key={issue}>{issue}</li>
          ))}
        </ul>
        <p className="setup-note">
          Use only the browser-safe Supabase publishable key. Never add the secret
          key to this file.
        </p>
      </section>
    </main>
  );
}

export function App() {
  const [selection, setSelection] = useState({ traceId: null, spanId: null });

  function selectTrace(traceId) {
    setSelection({ traceId, spanId: null });
  }

  if (!supabaseConfiguration.isValid) {
    return <ConfigurationError issues={supabaseConfiguration.issues} />;
  }

  return (
    <div className="app-shell">
      <aside className="trace-sidebar" aria-labelledby="recent-traces-title">
        <header className="sidebar-header">
          <div className="product-mark" aria-hidden="true">O</div>
          <div>
            <p className="product-name">Obeverfy</p>
            <p className="product-description">Agent observability</p>
          </div>
        </header>

        <div className="trace-list-heading">
          <h1 id="recent-traces-title">Recent traces</h1>
          <p>The latest agent executions from Supabase.</p>
        </div>

        <nav className="trace-list-region" aria-label="Trace history">
          <TraceList
            selectedTraceId={selection.traceId}
            onSelectTrace={selectTrace}
          />
        </nav>
      </aside>

      <main className="trace-workspace">
        {selection.traceId ? (
          <section className="workspace-state" aria-labelledby="selected-trace-title">
            <p className="workspace-context">Trace explorer</p>
            <h2 id="selected-trace-title">Trace selected</h2>
            <p>The span timeline and execution details will load in this workspace.</p>
            <dl className="selected-trace-reference">
              <dt>Trace ID</dt>
              <dd><code>{selection.traceId}</code></dd>
            </dl>
          </section>
        ) : (
          <section className="workspace-state" aria-labelledby="empty-workspace-title">
            <div className="workspace-symbol" aria-hidden="true">
              <span />
              <span />
              <span />
            </div>
            <h2 id="empty-workspace-title">Select a trace</h2>
            <p>Choose a recent execution to inspect its spans, timing, input, and output.</p>
          </section>
        )}
      </main>
    </div>
  );
}
