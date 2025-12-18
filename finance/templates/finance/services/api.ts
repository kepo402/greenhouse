import { DashboardResponse } from './types';

const BASE_URL =
  process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:8000/api' // local Django
    : '/api'; // production (same domain)

export async function fetchDashboard(month: string): Promise<DashboardResponse> {
  const response = await fetch(`${BASE_URL}/dashboard/?month=${month}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  return data;
}
