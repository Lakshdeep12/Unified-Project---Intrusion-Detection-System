export type Severity = "critical" | "high" | "medium" | "low";

export interface Alert {
  id: string;
  time: string;
  type: string;
  source: string;
  country: string;
  city: string;
  severity: Severity;
  signature: string;
}

const cities = [
  ["United States", "Ashburn"], ["Germany", "Frankfurt"], ["Brazil", "São Paulo"],
  ["China", "Beijing"], ["Russia", "Moscow"], ["India", "Mumbai"],
  ["Netherlands", "Amsterdam"], ["Singapore", "Singapore"], ["UK", "London"],
  ["France", "Paris"], ["Japan", "Tokyo"], ["Canada", "Toronto"],
];
const types = [
  "SYN Flood", "Port Scan", "Brute Force SSH", "SQL Injection",
  "XSS Probe", "DNS Tunnel", "Lateral Movement", "Privilege Escalation",
  "Ransomware C2", "Credential Stuffing",
];
const sigs = ["ET-2034981", "ET-1099821", "SN-77241", "ET-2042100", "OWASP-A03", "MITRE-T1190"];

export function randIp() {
  return `${1 + Math.floor(Math.random() * 254)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`;
}

export function makeAlert(id?: string): Alert {
  const [country, city] = cities[Math.floor(Math.random() * cities.length)];
  const r = Math.random();
  const severity: Severity = r > 0.85 ? "critical" : r > 0.6 ? "high" : r > 0.3 ? "medium" : "low";
  return {
    id: id ?? Math.random().toString(36).slice(2, 10),
    time: new Date().toISOString().slice(11, 19),
    type: types[Math.floor(Math.random() * types.length)],
    source: randIp(),
    country, city, severity,
    signature: sigs[Math.floor(Math.random() * sigs.length)],
  };
}

export const initialAlerts: Alert[] = Array.from({ length: 8 }, () => makeAlert());

export const initialTraffic = Array.from({ length: 60 }, (_, i) => ({
  t: i,
  attacks: Math.max(0, Math.round(8 + Math.sin(i / 5) * 4 + Math.random() * 6)),
  normal: Math.round(80 + Math.cos(i / 7) * 20 + Math.random() * 25),
}));
