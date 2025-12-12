from __future__ import annotations


def render_index() -> str:
    """
    Returns the HTML shell for the DBL Boundary Service UI.
    
    Main boundary UI layout with:
    - Resizable horizontal split
    - Collapsible JSON sections
    - Visual policy decisions
    - Improved API key UX
    - Syntax highlighting
    """
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>DBL Boundary Service</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      
      <!-- Syntax highlighting -->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>
      
      <style>
        * { box-sizing: border-box; }
        
        body {
          margin: 0;
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: #0b1120;
          color: #e5e7eb;
          overflow: hidden;
        }
        
        /* Main boundary UI layout - Resizable split */
        .root {
          display: flex;
          height: 100vh;
          position: relative;
        }
        
        .left {
          min-width: 20%;
          max-width: 80%;
          padding: 24px;
          background: radial-gradient(circle at top left, #111827, #020617);
          overflow-y: auto;
        }
        
        /* Resizable divider */
        .divider {
          width: 8px;
          background: #1f2937;
          cursor: col-resize;
          position: relative;
          transition: background 0.2s;
        }
        
        .divider:hover {
          background: #374151;
        }
        
        .divider::after {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 2px;
          height: 40px;
          background: #4b5563;
        }
        
        .right {
          flex: 1;
          padding: 24px;
          background: radial-gradient(circle at top right, #020617, #020617);
          overflow-y: auto;
        }
        
        h1 {
          font-size: 20px;
          margin: 0 0 4px 0;
        }
        
        h2 {
          font-size: 14px;
          margin: 16px 0 8px 0;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: #9ca3af;
        }
        
        p {
          font-size: 13px;
          color: #9ca3af;
          margin: 0 0 12px 0;
        }
        
        label {
          display: block;
          font-size: 12px;
          margin-bottom: 4px;
          color: #d1d5db;
        }
        
        input, textarea {
          width: 100%;
          padding: 8px 10px;
          border-radius: 8px;
          border: 1px solid #374151;
          background: #020617;
          color: #e5e7eb;
          font-size: 13px;
          outline: none;
        }
        
        input:focus, textarea:focus {
          border-color: #6366f1;
          box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.6);
        }
        
        textarea {
          resize: vertical;
          min-height: 120px;
          max-height: 260px;
          font-family: monospace;
        }
        
        .row {
          margin-bottom: 12px;
        }
        
        .button-row {
          margin-top: 8px;
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
        
        button {
          border-radius: 9999px;
          border: none;
          padding: 8px 16px;
          font-size: 13px;
          cursor: pointer;
          background: linear-gradient(135deg, #4f46e5, #06b6d4);
          color: #f9fafb;
          transition: opacity 0.2s;
        }
        
        button:hover:not(:disabled) {
          opacity: 0.9;
        }
        
        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        button.secondary {
          background: #111827;
          color: #e5e7eb;
          border: 1px solid #374151;
        }
        
        button.small {
          padding: 4px 12px;
          font-size: 11px;
        }
        
        .tagline {
          font-size: 12px;
          color: #6b7280;
          margin-bottom: 16px;
        }
        
        .badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 4px 8px;
          border-radius: 9999px;
          border: 1px solid #1f2937;
          background: rgba(15, 23, 42, 0.9);
          font-size: 11px;
          color: #9ca3af;
          margin-bottom: 10px;
        }
        
        .badge-dot {
          width: 7px;
          height: 7px;
          border-radius: 9999px;
          background: #22c55e;
        }
        
        /* API Key Status */
        .api-key-status {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 12px;
          border-radius: 8px;
          background: rgba(34, 197, 94, 0.1);
          border: 1px solid rgba(34, 197, 94, 0.3);
          font-size: 12px;
          color: #22c55e;
          margin-top: 8px;
        }
        
        .api-key-status-dot {
          width: 6px;
          height: 6px;
          border-radius: 9999px;
          background: #22c55e;
        }
        
        /* Panel and collapsible sections */
        .panel {
          border-radius: 12px;
          border: 1px solid #1f2937;
          padding: 14px;
          background: rgba(15, 23, 42, 0.9);
        }
        
        .panel h3 {
          margin: 0 0 12px 0;
          font-size: 14px;
        }
        
        /* Collapsible section */
        .collapsible-section {
          margin-bottom: 16px;
          border-bottom: 1px solid #1f2937;
          padding-bottom: 12px;
        }
        
        .collapsible-section:last-child {
          border-bottom: none;
        }
        
        .section-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          cursor: pointer;
          padding: 6px 0;
          user-select: none;
        }
        
        .section-header:hover {
          opacity: 0.8;
        }
        
        .section-title {
          font-size: 12px;
          color: #9ca3af;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          font-weight: 600;
        }
        
        .section-toggle {
          font-size: 18px;
          color: #6b7280;
          transition: transform 0.2s;
        }
        
        .section-toggle.collapsed {
          transform: rotate(-90deg);
        }
        
        .section-body {
          margin-top: 8px;
          overflow: hidden;
          transition: max-height 0.3s ease-out;
        }
        
        .section-body.collapsed {
          max-height: 0 !important;
          margin-top: 0;
        }
        
        .section-body pre {
          font-size: 11px;
          background: #020617;
          padding: 12px;
          border-radius: 6px;
          overflow-x: auto;
          margin: 0;
          font-family: 'Courier New', monospace;
        }
        
        /* Policy decision visual list */
        .policy-list {
          margin: 8px 0;
        }
        
        .policy-item {
          display: flex;
          align-items: start;
          gap: 12px;
          padding: 10px;
          margin-bottom: 8px;
          border-radius: 8px;
          background: rgba(15, 23, 42, 0.6);
          border: 1px solid #1f2937;
        }
        
        .policy-outcome {
          padding: 2px 8px;
          border-radius: 9999px;
          font-size: 10px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        
        .policy-outcome.allow {
          background: rgba(34, 197, 94, 0.2);
          color: #22c55e;
          border: 1px solid rgba(34, 197, 94, 0.4);
        }
        
        .policy-outcome.block {
          background: rgba(239, 68, 68, 0.2);
          color: #ef4444;
          border: 1px solid rgba(239, 68, 68, 0.4);
        }
        
        .policy-outcome.modify {
          background: rgba(245, 158, 11, 0.2);
          color: #f59e0b;
          border: 1px solid rgba(245, 158, 11, 0.4);
        }
        
        .policy-details {
          flex: 1;
        }
        
        .policy-name {
          font-size: 12px;
          font-weight: 600;
          color: #e5e7eb;
          margin-bottom: 4px;
        }
        
        .policy-reason {
          font-size: 11px;
          color: #9ca3af;
          line-height: 1.4;
        }
        
        /* Configuration section */
        .config-section {
          margin-bottom: 16px;
          padding: 12px;
          background: rgba(15, 23, 42, 0.4);
          border-radius: 8px;
          border: 1px solid #1f2937;
        }
        
        .config-section label {
          font-size: 11px;
          color: #d1d5db;
          display: block;
          margin-bottom: 4px;
        }
        
        .config-section select {
          width: 100%;
          padding: 6px 10px;
          border-radius: 6px;
          border: 1px solid #374151;
          background: #020617;
          color: #e5e7eb;
          font-size: 12px;
          outline: none;
        }
        
        .config-section select:focus {
          border-color: #6366f1;
        }
        
        /* Policy toggles */
        .policy-toggles {
          margin-top: 12px;
        }
        
        .policy-toggle-item {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 6px 0;
        }
        
        .policy-toggle-item input[type="checkbox"] {
          width: auto;
          cursor: pointer;
        }
        
        .policy-toggle-item label {
          font-size: 12px;
          color: #e5e7eb;
          cursor: pointer;
          margin: 0;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        
        /* Trace position toggle */
        .trace-controls {
          display: flex;
          gap: 8px;
          margin-bottom: 12px;
          padding: 8px;
          background: rgba(15, 23, 42, 0.6);
          border-radius: 8px;
        }
        
        .trace-controls label {
          font-size: 11px;
          color: #9ca3af;
          display: flex;
          align-items: center;
          gap: 4px;
        }
        
        .trace-controls select {
          background: #020617;
          color: #e5e7eb;
          border: 1px solid #374151;
          border-radius: 4px;
          padding: 2px 6px;
          font-size: 11px;
        }
        
        /* Outcome badges */
        .outcome-allow { color: #22c55e; }
        .outcome-modify { color: #f59e0b; }
        .outcome-block { color: #ef4444; }
        
        /* Syntax highlighting overrides for dark theme */
        .hljs {
          background: #020617 !important;
          padding: 12px !important;
        }
        
        /* Loading */
        .loading {
          color: #6b7280;
          font-style: italic;
        }
      </style>
    </head>
    <body>
      <!-- Main boundary UI layout -->
      <div class="root" id="root">
        <div class="left" id="leftPanel">
          <div class="badge">
            <span class="badge-dot"></span>
            <span>DBL Boundary Service</span>
          </div>
          <h1>Governed LLM boundary</h1>
          <p class="tagline">
            Small deterministic front end that will route your LLM calls through DBL and KL.
          </p>

          <div class="row">
            <h2>Connection</h2>
            <div id="apiKeySection">
              <label for="apiKey">OpenAI API key</label>
              <input id="apiKey" type="password" placeholder="sk-..." autocomplete="off" />
              <button id="saveKeyBtn" class="secondary small" style="margin-top: 8px;">Save key</button>
            </div>
            <div id="apiKeyStatus" class="api-key-status" style="display: none;">
              <span class="api-key-status-dot"></span>
              <span>API key configured</span>
              <button id="changeKeyBtn" class="small secondary">Change key</button>
            </div>
          </div>

          <div class="row">
            <h2>Prompt</h2>
            <label for="prompt">Prompt</label>
            <textarea id="prompt" placeholder="Ask the model something..."></textarea>
          </div>

          <div class="config-section">
            <label for="pipelineMode">Pipeline mode</label>
            <select id="pipelineMode">
              <option value="minimal">minimal – No policies (testing only)</option>
              <option value="basic_safety" selected>basic_safety – Light content safety only</option>
              <option value="standard">standard – Balanced safety + rate limiting</option>
              <option value="enterprise">enterprise – Strict safety, strict rate limiting</option>
            </select>
            
            <div class="policy-toggles">
              <div style="font-size: 11px; color: #9ca3af; margin-bottom: 6px;">Override policies:</div>
              <div class="policy-toggle-item">
                <label>
                  <input type="checkbox" id="policyContentSafety" />
                  <span>content_safety</span>
                </label>
              </div>
              <div class="policy-toggle-item">
                <label>
                  <input type="checkbox" id="policyRateLimit" />
                  <span>rate_limit</span>
                </label>
              </div>
              <div style="font-size: 10px; color: #6b7280; margin-top: 6px;">
                Leave unchecked to use preset policies
              </div>
            </div>
          </div>

          <div class="button-row">
            <button id="runBtn" disabled>Run through boundary</button>
            <button class="secondary" id="dryRunBtn">Dry run (no LLM)</button>
          </div>
          <p style="font-size: 11px; margin-top: 10px;">
            "Run" requires an API key. "Dry run" tests the full DBL+KL flow without calling the LLM.
          </p>
        </div>
        
        <!-- Resizable divider -->
        <div class="divider" id="divider"></div>
        
        <div class="right" id="rightPanel">
          <div class="panel" id="insightsPanel">
            <h3>Execution and policy insights</h3>
            <p>
              Run a prompt to see the full request lifecycle with collapsible sections and visual policy decisions.
            </p>
            <p style="margin-top: 8px; font-size: 11px;">
              Use "Dry run" to test the flow without calling the LLM.
            </p>
          </div>
        </div>
      </div>

      <script>
      // State
      let hasApiKey = false;
      let tracePosition = 'bottom'; // 'top' or 'bottom'
      let pipelineMode = 'basic_safety';  // Default mode
      let policyOverride = false; // User has manually toggled policies
      let enabledPolicies = new Set(); // Set of enabled policy names
      let collapsedSections = {
        boundaryContext: true,
        policyDecisions: true,
        psiDefinition: true,
        llmPayload: true,
        llmResult: false,
        trace: false
      };

      // Elements
      const keyInput = document.getElementById("apiKey");
      const promptInput = document.getElementById("prompt");
      const runBtn = document.getElementById("runBtn");
      const dryRunBtn = document.getElementById("dryRunBtn");
      const insightsPanel = document.getElementById("insightsPanel");
      const saveKeyBtn = document.getElementById("saveKeyBtn");
      const changeKeyBtn = document.getElementById("changeKeyBtn");
      const apiKeySection = document.getElementById("apiKeySection");
      const apiKeyStatus = document.getElementById("apiKeyStatus");
      const leftPanel = document.getElementById("leftPanel");
      const rightPanel = document.getElementById("rightPanel");
      const divider = document.getElementById("divider");
      const root = document.getElementById("root");
      const pipelineModeSelect = document.getElementById("pipelineMode");
      const policyContentSafety = document.getElementById("policyContentSafety");
      const policyRateLimit = document.getElementById("policyRateLimit");

      // Resizable split implementation
      let isResizing = false;
      let startX = 0;
      let startLeftWidth = 0;

      divider.addEventListener('mousedown', (e) => {
        isResizing = true;
        startX = e.clientX;
        startLeftWidth = leftPanel.offsetWidth;
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
      });

      document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        
        const delta = e.clientX - startX;
        const newLeftWidth = startLeftWidth + delta;
        const totalWidth = root.offsetWidth;
        const minWidth = totalWidth * 0.2;
        const maxWidth = totalWidth * 0.8;
        
        if (newLeftWidth >= minWidth && newLeftWidth <= maxWidth) {
          leftPanel.style.width = newLeftWidth + 'px';
          leftPanel.style.flexShrink = '0';
        }
      });

      document.addEventListener('mouseup', () => {
        if (isResizing) {
          isResizing = false;
          document.body.style.cursor = '';
        }
      });

      // API Key UX
      saveKeyBtn.addEventListener("click", async () => {
        const value = keyInput.value.trim();
        if (value.length < 10) {
          alert("Please enter a valid API key");
          return;
        }

        try {
          const res = await fetch("/set-key", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ api_key: value })
          });
          
          if (res.ok) {
            hasApiKey = true;
            runBtn.disabled = false;
            
            // Hide input, show status
            apiKeySection.style.display = 'none';
            apiKeyStatus.style.display = 'flex';
            keyInput.value = '';
          } else {
            alert("Failed to save API key");
          }
        } catch (err) {
          console.error("Failed to set API key", err);
          alert("Error saving API key");
        }
      });

      changeKeyBtn.addEventListener("click", () => {
        apiKeySection.style.display = 'block';
        apiKeyStatus.style.display = 'none';
        hasApiKey = false;
        runBtn.disabled = true;
        keyInput.focus();
      });

      // Pipeline mode change
      pipelineModeSelect.addEventListener("change", (e) => {
        pipelineMode = e.target.value;
        
        // If user hasn't manually toggled policies, update checkboxes to reflect preset
        if (!policyOverride) {
          updateCheckboxesForPreset(pipelineMode);
        }
      });

      // Policy toggle handlers
      policyContentSafety.addEventListener("change", (e) => {
        policyOverride = true;
        if (e.target.checked) {
          enabledPolicies.add("content_safety");
        } else {
          enabledPolicies.delete("content_safety");
        }
      });

      policyRateLimit.addEventListener("change", (e) => {
        policyOverride = true;
        if (e.target.checked) {
          enabledPolicies.add("rate_limit");
        } else {
          enabledPolicies.delete("rate_limit");
        }
      });

      // Update checkboxes based on preset
      function updateCheckboxesForPreset(mode) {
        // Sync checkboxes with preset policies (visual feedback only)
        const presets = {
          'minimal': [],
          'basic_safety': ['content_safety'],
          'standard': ['content_safety', 'rate_limit'],
          'enterprise': ['content_safety', 'rate_limit']
        };
        
        const preset = presets[mode] || presets['basic_safety'];
        policyContentSafety.checked = preset.includes('content_safety');
        policyRateLimit.checked = preset.includes('rate_limit');
        
        // Update internal state only if not overridden
        if (!policyOverride) {
          enabledPolicies.clear();
          preset.forEach(p => enabledPolicies.add(p));
        }
      }

      // Initialize with default preset
      updateCheckboxesForPreset('basic_safety');

      // Run execution
      async function executeRun(dryRun) {
        const prompt = promptInput.value.trim();
        if (!prompt) {
          alert("Please enter a prompt");
          return;
        }

        insightsPanel.innerHTML = '<p class="loading">Running...</p>';

        // Build request body
        const body = {
          prompt,
          dry_run: dryRun,
          pipeline_mode: pipelineMode
        };
        
        // Only send enabled_policies if user has overridden
        if (policyOverride && enabledPolicies.size > 0) {
          body.enabled_policies = Array.from(enabledPolicies);
        }

        try {
          const res = await fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
          });
          const data = await res.json();
          renderInsights(data);
        } catch (err) {
          insightsPanel.innerHTML = `<p style="color: #ef4444;">Error: ${err.message}</p>`;
        }
      }

      runBtn.addEventListener("click", () => executeRun(false));
      dryRunBtn.addEventListener("click", () => executeRun(true));

      // Render insights with all UX improvements
      function renderInsights(data) {
        const s = data.snapshot;
        const blocked = data.blocked;
        const statusBadge = blocked 
          ? '<span style="color:#ef4444;font-weight:600;">BLOCKED</span>' 
          : '<span style="color:#22c55e;font-weight:600;">ALLOWED</span>';
        
        // Trace controls
        const traceControls = `
          <div class="trace-controls">
            <label>
              Trace position:
              <select id="tracePositionSelect" onchange="updateTracePosition(this.value)">
                <option value="top" ${tracePosition === 'top' ? 'selected' : ''}>Top</option>
                <option value="bottom" ${tracePosition === 'bottom' ? 'selected' : ''}>Bottom</option>
              </select>
            </label>
          </div>
        `;
        
        // Build sections
        const traceSection = renderTraceSection(s);
        const sections = [
          tracePosition === 'top' ? traceSection : null,
          renderResponseSection(data, statusBadge),
          renderPolicyDecisionsSection(s),
          renderOutcomeSection(s),
          renderBoundaryContextSection(s),
          renderPsiDefinitionSection(s),
          s.llm_payload ? renderLlmPayloadSection(s) : null,
          s.llm_result ? renderLlmResultSection(s) : null,
          tracePosition === 'bottom' ? traceSection : null,
        ].filter(x => x !== null).join('');
        
        insightsPanel.innerHTML = `
          <h3>Result: ${statusBadge}</h3>
          ${traceControls}
          ${sections}
        `;
        
        // Highlight all code blocks
        document.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightElement(block);
        });
        
        // Attach collapse handlers
        attachCollapseHandlers();
      }

      function renderResponseSection(data, statusBadge) {
        return renderCollapsibleSection(
          'Response',
          `<pre>${escapeHtml(data.content)}</pre>`,
          'response',
          false // Always open
        );
      }

      function renderPolicyDecisionsSection(s) {
        const decisions = s.policy_decisions || [];
        
        // Visual policy list
        const policyList = decisions.map(d => `
          <div class="policy-item">
            <span class="policy-outcome ${d.outcome}">${d.outcome}</span>
            <div class="policy-details">
              <div class="policy-name">${d.policy || 'unknown'}</div>
              <div class="policy-reason">${d.reason || 'No reason provided'}</div>
            </div>
          </div>
        `).join('');
        
        const jsonContent = `<code class="language-json">${JSON.stringify(decisions, null, 2)}</code>`;
        
        return renderCollapsibleSection(
          `Policy Decisions (${decisions.length})`,
          `
            <div class="policy-list">${policyList}</div>
            <details style="margin-top: 12px;">
              <summary style="cursor: pointer; font-size: 11px; color: #6b7280;">Show raw JSON</summary>
              <pre style="margin-top: 8px;">${jsonContent}</pre>
            </details>
          `,
          'policyDecisions',
          collapsedSections.policyDecisions
        );
      }

      function renderOutcomeSection(s) {
        return `
          <div class="collapsible-section">
            <div class="section-title">
              DBL Outcome: <span class="outcome-${s.dbl_outcome}">${s.dbl_outcome.toUpperCase()}</span>
            </div>
          </div>
        `;
      }

      function renderBoundaryContextSection(s) {
        const content = `<code class="language-json">${JSON.stringify(s.boundary_context, null, 2)}</code>`;
        return renderCollapsibleSection('BoundaryContext', `<pre>${content}</pre>`, 'boundaryContext', collapsedSections.boundaryContext);
      }

      function renderPsiDefinitionSection(s) {
        const content = `<code class="language-json">${JSON.stringify(s.psi_definition, null, 2)}</code>`;
        return renderCollapsibleSection('PsiDefinition', `<pre>${content}</pre>`, 'psiDefinition', collapsedSections.psiDefinition);
      }

      function renderLlmPayloadSection(s) {
        const content = `<code class="language-json">${JSON.stringify(s.llm_payload, null, 2)}</code>`;
        return renderCollapsibleSection('LLM Payload', `<pre>${content}</pre>`, 'llmPayload', collapsedSections.llmPayload);
      }

      function renderLlmResultSection(s) {
        const content = `<code class="language-json">${JSON.stringify(s.llm_result, null, 2)}</code>`;
        return renderCollapsibleSection('LLM Result', `<pre>${content}</pre>`, 'llmResult', collapsedSections.llmResult);
      }

      function renderTraceSection(s) {
        const content = `
          <p style="font-size: 11px; margin: 4px 0;"><strong>Request ID:</strong> ${s.request_id}</p>
          <p style="font-size: 11px; margin: 4px 0;"><strong>Execution Trace:</strong> ${s.execution_trace_id || 'N/A'}</p>
          <p style="font-size: 11px; margin: 4px 0;"><strong>Timestamp:</strong> ${s.timestamp}</p>
          <p style="font-size: 11px; margin: 4px 0;"><strong>Dry Run:</strong> ${s.dry_run}</p>
        `;
        return renderCollapsibleSection('Trace', content, 'trace', collapsedSections.trace);
      }

      function renderCollapsibleSection(title, content, key, collapsed) {
        const bodyId = `section-body-${key}`;
        const toggleId = `section-toggle-${key}`;
        
        return `
          <div class="collapsible-section">
            <div class="section-header" onclick="toggleSection('${key}')">
              <div class="section-title">${title}</div>
              <div class="section-toggle ${collapsed ? 'collapsed' : ''}" id="${toggleId}">▼</div>
            </div>
            <div class="section-body ${collapsed ? 'collapsed' : ''}" id="${bodyId}">
              ${content}
            </div>
          </div>
        `;
      }

      function toggleSection(key) {
        collapsedSections[key] = !collapsedSections[key];
        const body = document.getElementById(`section-body-${key}`);
        const toggle = document.getElementById(`section-toggle-${key}`);
        
        if (collapsedSections[key]) {
          body.classList.add('collapsed');
          toggle.classList.add('collapsed');
        } else {
          body.classList.remove('collapsed');
          toggle.classList.remove('collapsed');
          // Set max-height for animation
          body.style.maxHeight = body.scrollHeight + 'px';
        }
      }

      function attachCollapseHandlers() {
        // Set initial max-heights for non-collapsed sections
        Object.keys(collapsedSections).forEach(key => {
          if (!collapsedSections[key]) {
            const body = document.getElementById(`section-body-${key}`);
            if (body) {
              body.style.maxHeight = body.scrollHeight + 'px';
            }
          }
        });
      }

      function updateTracePosition(position) {
        tracePosition = position;
        // Re-render would happen on next execution
      }

      function escapeHtml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      }

      // Make functions globally available for inline handlers
      window.toggleSection = toggleSection;
      window.updateTracePosition = updateTracePosition;
      </script>
    </body>
    </html>
    """
