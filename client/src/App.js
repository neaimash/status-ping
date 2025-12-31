import { useState } from "react";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStatus = async (type) => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`http://127.0.0.1:8000/status/${type}`);
      if (!res.ok) {
        throw new Error("Request failed");
      }
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Status Ping</h1>

      <button onClick={() => fetchStatus("vapp")}>
        Check vApp
      </button>

      <button onClick={() => fetchStatus("fapp")} style={{ marginLeft: 10 }}>
        Check fApp
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}
    </div>
  );
}

export default App;
