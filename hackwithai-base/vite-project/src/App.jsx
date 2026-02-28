import { useState, useEffect } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeText = async (value) => {
    if (!value.trim()) {
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: value }),
      });

      if (!response.ok) throw new Error("API request failed");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Backend not responding.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delay = setTimeout(() => {
      analyzeText(text);
    }, 500);
    return () => clearTimeout(delay);
  }, [text]);

  const getRiskColor = (level) => {
    if (level === "High") return "#ef4444";
    if (level === "Medium") return "#f59e0b";
    return "#22c55e";
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f3f4f6",
        fontFamily: "Inter, sans-serif",
        padding: "40px",
      }}
    >
      <h2 style={{ marginBottom: "30px" }}>
        Context-aware privacy exposure detection
      </h2>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 420px", gap: "40px" }}>
        {/* LEFT SIDE */}
        <div>
          <textarea
            rows="8"
            style={{
              width: "100%",
              padding: "16px",
              borderRadius: "12px",
              border: "1px solid #d1d5db",
              fontSize: "15px",
              resize: "none",
            }}
            placeholder="Paste social media content..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />

          {loading && <p style={{ marginTop: "10px" }}>Analyzing...</p>}

          {result && (
            <div
              style={{
                marginTop: "25px",
                padding: "25px",
                background: "white",
                borderRadius: "16px",
                boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ fontSize: "56px", fontWeight: "700" }}>
                  {result.score}
                </div>

                <div
                  style={{
                    padding: "6px 14px",
                    borderRadius: "20px",
                    background: "#fee2e2",
                    color: getRiskColor(result.risk_level),
                    fontWeight: "600",
                  }}
                >
                  {result.risk_level}
                </div>
              </div>

              {/* UPDATED BAR SECTION */}
              <div style={{ marginTop: "15px" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "14px",
                    marginBottom: "6px",
                  }}
                >
                  <span>Exposure Level</span>
                  <span>{result.score}/100</span>
                </div>

                <div
                  style={{
                    height: "8px",
                    background: "#e5e7eb",
                    borderRadius: "6px",
                  }}
                >
                  <div
                    style={{
                      width: `${result.score}%`,
                      height: "100%",
                      background: getRiskColor(result.risk_level),
                      borderRadius: "6px",
                    }}
                  />
                </div>
              </div>

              <p style={{ marginTop: "15px", color: "#6b7280" }}>
                {result.risk_summary}
              </p>
            </div>
          )}
        </div>

        {/* RIGHT SIDE */}
        {result && (
          <div>
            <h3 style={{ marginBottom: "15px" }}>CATEGORY BREAKDOWN</h3>

            {Object.entries(result.breakdown).map(([key, value]) => {
              const percent = Math.round(value * 100);

              return (
                <div
                  key={key}
                  style={{
                    background: "white",
                    padding: "16px",
                    borderRadius: "14px",
                    marginBottom: "15px",
                    boxShadow: "0 8px 20px rgba(0,0,0,0.05)",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <strong style={{ textTransform: "capitalize" }}>{key}</strong>
                    <span>{percent}%</span>
                  </div>

                  <div
                    style={{
                      marginTop: "8px",
                      height: "6px",
                      background: "#e5e7eb",
                      borderRadius: "6px",
                    }}
                  >
                    <div
                      style={{
                        width: `${percent}%`,
                        height: "100%",
                        background: "#3b82f6",
                        borderRadius: "6px",
                      }}
                    />
                  </div>
                </div>
              );
            })}

            {/* RECOMMENDATIONS */}
            <h3 style={{ marginTop: "25px" }}>RECOMMENDATIONS</h3>

            {result.recommendations.map((rec, i) => (
              <div
                key={i}
                style={{
                  padding: "12px",
                  background: "#fff7ed",
                  border: "1px solid #facc15",
                  borderRadius: "12px",
                  marginBottom: "12px",
                }}
              >
                ⚠ {rec}
              </div>
            ))}

            {/* 🆕 ADVERSARIAL RISK SIMULATION */}
            {result.attacker_inference && result.attacker_inference.length > 0 && (
              <>
                <h3 style={{ marginTop: "30px" }}>
                  Adversarial Risk Simulation
                </h3>

                <div
                  style={{
                    background: "#1f2937",
                    color: "white",
                    padding: "18px",
                    borderRadius: "14px",
                    marginTop: "12px",
                  }}
                >
                  <p style={{ marginBottom: "12px", fontWeight: "600" }}>
                    What an attacker can infer from this post:
                  </p>

                  <ul style={{ paddingLeft: "18px" }}>
                    {result.attacker_inference.map((item, i) => (
                      <li key={i} style={{ marginBottom: "8px" }}>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
