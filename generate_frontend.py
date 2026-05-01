import os

def create_frontend():
    base_dir = r"d:\Unfied Project-1\Dashboard"
    
    tailwind_path = os.path.join(base_dir, "tailwind.config.js")
    with open(tailwind_path, "w") as f:
        f.write("""/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
""")

    index_css_path = os.path.join(base_dir, "src", "index.css")
    with open(index_css_path, "w") as f:
        f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  background-color: #0f172a;
  color: #f8fafc;
  font-family: 'Inter', sans-serif;
}
""")

    app_jsx_path = os.path.join(base_dir, "src", "App.jsx")
    with open(app_jsx_path, "w") as f:
        f.write("""import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar
} from 'recharts';

function App() {
  const [stats, setStats] = useState({ total_events: 0, total_attacks: 0, attack_rate: 0 });
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const fetchData = async () => {
    try {
      const statRes = await axios.get('http://localhost:8000/api/stats');
      setStats(statRes.data);
      
      const logRes = await axios.get('http://localhost:8000/api/logs?limit=10');
      setLogs(logRes.data.logs || []);
      
      const alertRes = await axios.get('http://localhost:8000/api/alerts?limit=5');
      setAlerts(alertRes.data.alerts || []);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // Polling every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const dummyChartData = [
    { time: '10:00', attacks: 5 },
    { time: '10:05', attacks: 10 },
    { time: '10:10', attacks: 2 },
    { time: '10:15', attacks: 8 },
    { time: '10:20', attacks: stats.total_attacks },
  ];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-blue-400">IDS Security Dashboard</h1>
        <p className="text-slate-400">Real-time Intrusion Detection Monitoring</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
          <h2 className="text-xl text-slate-300">Total Events</h2>
          <p className="text-4xl font-bold text-blue-500 mt-2">{stats.total_events}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
          <h2 className="text-xl text-slate-300">Detected Attacks</h2>
          <p className="text-4xl font-bold text-red-500 mt-2">{stats.total_attacks}</p>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
          <h2 className="text-xl text-slate-300">Attack Rate</h2>
          <p className="text-4xl font-bold text-yellow-500 mt-2">{stats.attack_rate}%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700 h-96">
          <h2 className="text-xl mb-4 font-semibold text-slate-200">Attack Frequency</h2>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={dummyChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
              <Legend />
              <Line type="monotone" dataKey="attacks" stroke="#ef4444" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700 overflow-y-auto h-96">
          <h2 className="text-xl mb-4 font-semibold text-slate-200">Recent Alerts</h2>
          {alerts.length === 0 ? (
            <p className="text-slate-400">No recent alerts.</p>
          ) : (
            <ul className="space-y-3">
              {alerts.map((a, i) => (
                <li key={i} className="p-3 bg-red-900/30 border border-red-700/50 rounded-lg flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-red-400">Alert</span>
                    <p className="text-sm text-slate-300">{a.message}</p>
                  </div>
                  <span className="text-xs text-slate-500">{new Date(a.timestamp).toLocaleTimeString()}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700 overflow-x-auto">
        <h2 className="text-xl mb-4 font-semibold text-slate-200">Recent Logs</h2>
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400">
              <th className="pb-3 px-4">Time</th>
              <th className="pb-3 px-4">Prediction</th>
              <th className="pb-3 px-4">Confidence</th>
              <th className="pb-3 px-4">Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan="4" className="py-4 px-4 text-center text-slate-500">No logs available.</td>
              </tr>
            ) : (
              logs.map((log, i) => (
                <tr key={i} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                  <td className="py-3 px-4 text-slate-300">{new Date(log.timestamp).toLocaleTimeString()}</td>
                  <td className="py-3 px-4 font-mono">{log.prediction}</td>
                  <td className="py-3 px-4">{log.confidence}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs ${log.is_attack ? 'bg-red-900/50 text-red-400' : 'bg-green-900/50 text-green-400'}`}>
                      {log.is_attack ? 'ATTACK' : 'NORMAL'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
""")

if __name__ == "__main__":
    create_frontend()
    print("Frontend files created.")
