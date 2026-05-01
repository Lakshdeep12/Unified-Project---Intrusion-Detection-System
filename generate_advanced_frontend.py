import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def create_frontend():
    base = r"d:\Unfied Project-1\Dashboard\src"
    
    # 1. Main Entry Points
    write_file(os.path.join(base, "main.jsx"), """import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
""")

    write_file(os.path.join(base, "App.jsx"), """import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Analytics from './pages/Analytics';
import Login from './pages/Login';
import Register from './pages/Register';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/login" />;
  return children;
}

function App() {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';

  if (isAuthPage) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    );
  }

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
            <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
export default App;
""")

    # 2. Components
    write_file(os.path.join(base, "components", "Sidebar.jsx"), """import { NavLink } from 'react-router-dom';
import { ShieldAlert, LayoutDashboard, Activity, Settings, Wrench } from 'lucide-react';

export default function Sidebar() {
  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
      <div className="p-6 flex items-center gap-3 border-b border-slate-800">
        <ShieldAlert className="w-8 h-8 text-blue-500" />
        <span className="text-xl font-bold tracking-wider">NEXUS<span className="text-blue-500">IDS</span></span>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        <NavLink to="/" className={({isActive}) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600/20 text-blue-400' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'}`}>
          <LayoutDashboard className="w-5 h-5" /> Dashboard
        </NavLink>
        <NavLink to="/analytics" className={({isActive}) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600/20 text-blue-400' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'}`}>
          <Activity className="w-5 h-5" /> Analytics
        </NavLink>
      </nav>
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        System Core v2.4.1
      </div>
    </div>
  );
}
""")

    write_file(os.path.join(base, "components", "Navbar.jsx"), """import { Bell, User, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6">
      <div className="flex items-center gap-2">
        <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
        <span className="text-sm font-medium text-slate-300">System Online</span>
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-slate-400 hover:text-slate-200 transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <div className="h-8 w-px bg-slate-700" />
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
            <User className="w-4 h-4 text-slate-400" />
          </div>
          <button onClick={handleLogout} className="text-sm text-slate-400 hover:text-red-400 transition-colors">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
""")

    # 3. Pages (Auth)
    write_file(os.path.join(base, "pages", "Login.jsx"), """import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Shield } from 'lucide-react';

export default function Login() {
  const [user, setUser] = useState({ username: '', password: '' });
  const [err, setErr] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', user.username);
      formData.append('password', user.password);
      const res = await axios.post('http://localhost:8000/auth/login', formData);
      localStorage.setItem('token', res.data.access_token);
      navigate('/');
    } catch (error) {
      setErr('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <div className="w-full max-w-md p-8 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl">
        <div className="flex flex-col items-center mb-8">
          <Shield className="w-12 h-12 text-blue-500 mb-4" />
          <h1 className="text-2xl font-bold text-slate-100">SOC Access Gateway</h1>
        </div>
        {err && <div className="p-3 mb-4 text-sm text-red-400 bg-red-950/50 border border-red-900 rounded-lg">{err}</div>}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Operator ID</label>
            <input type="text" className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg focus:border-blue-500 focus:outline-none text-slate-200"
              value={user.username} onChange={e=>setUser({...user, username: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Passcode</label>
            <input type="password" className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg focus:border-blue-500 focus:outline-none text-slate-200"
              value={user.password} onChange={e=>setUser({...user, password: e.target.value})} required />
          </div>
          <button className="w-full p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
            Authenticate
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          No access? <Link to="/register" className="text-blue-400 hover:underline">Request clearance</Link>
        </p>
      </div>
    </div>
  );
}
""")

    write_file(os.path.join(base, "pages", "Register.jsx"), """import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Shield } from 'lucide-react';

export default function Register() {
  const [user, setUser] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/auth/register', user);
      navigate('/login');
    } catch (error) {
      alert("Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <div className="w-full max-w-md p-8 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl">
        <div className="flex flex-col items-center mb-8">
          <Shield className="w-12 h-12 text-blue-500 mb-4" />
          <h1 className="text-2xl font-bold text-slate-100">Request Clearance</h1>
        </div>
        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Desired Operator ID</label>
            <input type="text" className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg focus:border-blue-500 focus:outline-none text-slate-200"
              value={user.username} onChange={e=>setUser({...user, username: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Passcode</label>
            <input type="password" className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg focus:border-blue-500 focus:outline-none text-slate-200"
              value={user.password} onChange={e=>setUser({...user, password: e.target.value})} required />
          </div>
          <button className="w-full p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
            Submit Request
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          Already authorized? <Link to="/login" className="text-blue-400 hover:underline">Authenticate here</Link>
        </p>
      </div>
    </div>
  );
}
""")

    # 4. Pages (Home)
    write_file(os.path.join(base, "pages", "Home.jsx"), """import { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, ShieldAlert, Zap, Globe, RefreshCw } from 'lucide-react';

export default function Home() {
  const [stats, setStats] = useState({ total_packets: 0, attacks_detected: 0, normal_traffic: 0, status: 'Running' });
  const [attackRate, setAttackRate] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [config, setConfig] = useState({ attack_threshold: 0.8, mode: 'Hybrid', replay_speed: 1 });

  const fetchData = async () => {
    try {
      const st = await axios.get('http://localhost:8000/api/live-stats');
      setStats(st.data);
      const ar = await axios.get('http://localhost:8000/api/attack-rate');
      setAttackRate(ar.data.history);
      const al = await axios.get('http://localhost:8000/api/alerts/recent');
      setAlerts(al.data.alerts);
      const lg = await axios.get('http://localhost:8000/api/logs?limit=5');
      setLogs(lg.data.logs);
    } catch (e) { console.error(e); }
  };

  const fetchConfig = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/config');
      setConfig(res.data);
    } catch (e) {}
  };

  useEffect(() => {
    fetchData();
    fetchConfig();
    const intv = setInterval(fetchData, 2000);
    return () => clearInterval(intv);
  }, []);

  const updateConfig = async (key, val) => {
    const newConf = { ...config, [key]: val };
    setConfig(newConf);
    try { await axios.post('http://localhost:8000/api/config/update', newConf); } catch (e) {}
  };

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { title: "Total Packets", val: stats.total_packets, icon: Activity, col: "text-blue-500" },
          { title: "Attacks Detected", val: stats.attacks_detected, icon: ShieldAlert, col: "text-red-500" },
          { title: "Normal Traffic", val: stats.normal_traffic, icon: Zap, col: "text-green-500" },
          { title: "System Status", val: stats.status, icon: Globe, col: "text-indigo-500" },
        ].map((s, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-sm flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">{s.title}</p>
              <p className={`text-3xl font-bold mt-2 ${s.col}`}>{s.val}</p>
            </div>
            <div className={`p-3 rounded-lg bg-slate-950/50 border border-slate-800 ${s.col}`}>
              <s.icon className="w-6 h-6" />
            </div>
          </div>
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Attack Rate Graph */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold">Live Attack Rate</h2>
            <div className="flex items-center gap-2 text-xs text-red-400 animate-pulse">
              <div className="w-2 h-2 rounded-full bg-red-500" /> Live
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={attackRate}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="time" hide />
                <YAxis stroke="#475569" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#fff' }} />
                <Line type="monotone" dataKey="attacks" stroke="#ef4444" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Live Alerts Panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col">
          <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-500" /> Recent Alerts
          </h2>
          <div className="flex-1 overflow-y-auto space-y-3 pr-2">
            {alerts.map((a, i) => (
              <div key={i} className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                <div className="flex justify-between items-start mb-1">
                  <span className="font-semibold text-red-400 text-sm">{a.attack_type}</span>
                  <span className="text-xs text-slate-500">{a.timestamp.split(' ')[1]}</span>
                </div>
                <div className="text-xs text-slate-300">Target: <span className="font-mono text-slate-400">{a.source_ip}</span></div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Bottom Grid: Logs & Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Logs Table */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 overflow-hidden flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold">Traffic Logs</h2>
            <button onClick={fetchData} className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-slate-300">
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="pb-3 px-2 font-medium">Time</th>
                  <th className="pb-3 px-2 font-medium">Source IP</th>
                  <th className="pb-3 px-2 font-medium">Dest IP</th>
                  <th className="pb-3 px-2 font-medium">Prediction</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {logs.map((lg, i) => (
                  <tr key={i} className="hover:bg-slate-800/50 transition-colors">
                    <td className="py-3 px-2 text-slate-300">{lg.timestamp.split(' ')[1]}</td>
                    <td className="py-3 px-2 font-mono text-slate-400">{lg.source_ip}</td>
                    <td className="py-3 px-2 font-mono text-slate-400">{lg.dest_ip}</td>
                    <td className="py-3 px-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${lg.is_attack ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                        {lg.prediction}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* System Controls Panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <Settings className="w-5 h-5 text-slate-400" /> System Controls
          </h2>
          <div className="space-y-6">
            <div>
              <label className="flex justify-between text-sm text-slate-400 mb-2">
                <span>Attack Threshold</span>
                <span className="text-blue-400 font-medium">{config.attack_threshold}</span>
              </label>
              <input type="range" min="0" max="1" step="0.05" value={config.attack_threshold} 
                onChange={e => updateConfig('attack_threshold', parseFloat(e.target.value))}
                className="w-full accent-blue-500" />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Detection Mode</label>
              <select value={config.mode} onChange={e => updateConfig('mode', e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 text-slate-200 text-sm rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 outline-none">
                <option value="Supervised">Supervised (Alpha)</option>
                <option value="Unsupervised">Unsupervised (Beta)</option>
                <option value="Hybrid">Hybrid</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Replay Speed (x{config.replay_speed})</label>
              <div className="flex gap-2">
                {[1, 2, 5, 10].map(s => (
                  <button key={s} onClick={() => updateConfig('replay_speed', s)}
                    className={`flex-1 py-1.5 rounded-md text-sm font-medium transition-colors ${config.replay_speed === s ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>
                    {s}x
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
""")

    # 5. Pages (Analytics)
    write_file(os.path.join(base, "pages", "Analytics.jsx"), """import { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Analytics() {
  const [cm, setCm] = useState(null);
  const [roc, setRoc] = useState([]);
  const [fi, setFi] = useState([]);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const cmRes = await axios.get('http://localhost:8000/api/metrics/confusion-matrix');
        setCm(cmRes.data);
        const rocRes = await axios.get('http://localhost:8000/api/metrics/roc');
        const formattedRoc = rocRes.data.fpr.map((v, i) => ({ fpr: v, tpr: rocRes.data.tpr[i] }));
        setRoc(formattedRoc);
        const fiRes = await axios.get('http://localhost:8000/api/metrics/feature-importance');
        setFi(fiRes.data.features);
      } catch (e) {}
    };
    fetchMetrics();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Model Analytics</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Confusion Matrix */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-6">Confusion Matrix</h2>
          {cm && (
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-green-900/30 border border-green-500/30 p-6 rounded-lg text-center">
                <p className="text-slate-400 text-sm">True Normal</p>
                <p className="text-3xl font-bold text-green-400 mt-2">{cm.matrix[0][0]}</p>
              </div>
              <div className="bg-red-900/30 border border-red-500/30 p-6 rounded-lg text-center">
                <p className="text-slate-400 text-sm">False Attack</p>
                <p className="text-3xl font-bold text-red-400 mt-2">{cm.matrix[0][1]}</p>
              </div>
              <div className="bg-yellow-900/30 border border-yellow-500/30 p-6 rounded-lg text-center">
                <p className="text-slate-400 text-sm">False Normal</p>
                <p className="text-3xl font-bold text-yellow-400 mt-2">{cm.matrix[1][0]}</p>
              </div>
              <div className="bg-blue-900/30 border border-blue-500/30 p-6 rounded-lg text-center">
                <p className="text-slate-400 text-sm">True Attack</p>
                <p className="text-3xl font-bold text-blue-400 mt-2">{cm.matrix[1][1]}</p>
              </div>
            </div>
          )}
        </div>

        {/* ROC Curve */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-6">ROC Curve</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={roc}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="fpr" type="number" domain={[0, 1]} stroke="#475569" fontSize={12} />
                <YAxis domain={[0, 1]} stroke="#475569" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }} />
                <Line type="monotone" dataKey="tpr" stroke="#3b82f6" strokeWidth={2} dot={false} />
                <Line type="linear" dataKey="fpr" stroke="#64748b" strokeDasharray="5 5" strokeWidth={1} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Feature Importance */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold mb-6">Feature Importance</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={fi} layout="vertical" margin={{ left: 100 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#475569" fontSize={12} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={12} width={120} />
                <Tooltip cursor={{fill: '#1e293b'}} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }} />
                <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
""")

if __name__ == "__main__":
    create_frontend()
    print("Advanced frontend generated.")
