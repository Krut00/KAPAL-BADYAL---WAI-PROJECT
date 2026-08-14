import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts';
import './CCCChart.css';

export function CCCComponentsChart({ data }) {
  const chartData = [
    {
      name: 'Components',
      'Inventory Days': data.inventory_days,
      'Receivable Days': data.receivable_days,
      'Payable Days': data.payable_days,
    }
  ];

  return (
    <div className="chart-container">
      <h3>CCC Components Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Inventory Days" fill="#667eea" />
          <Bar dataKey="Receivable Days" fill="#764ba2" />
          <Bar dataKey="Payable Days" fill="#f093fb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function CCCTrendChart({ data }) {
  if (!data || data.length === 0) return <div>No trend data available</div>;

  return (
    <div className="chart-container">
      <h3>CCC Trend Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="ccc" stroke="#667eea" strokeWidth={2} name="CCC" />
          <Line type="monotone" dataKey="inventory_days" stroke="#764ba2" strokeWidth={2} name="Inventory Days" />
          <Line type="monotone" dataKey="receivable_days" stroke="#f093fb" strokeWidth={2} name="Receivable Days" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function ComparisonChart({ company1, company2 }) {
  const chartData = [
    {
      metric: 'Inventory Days',
      [company1.name]: company1.ccc.inventory_days,
      [company2.name]: company2.ccc.inventory_days,
    },
    {
      metric: 'Receivable Days',
      [company1.name]: company1.ccc.receivable_days,
      [company2.name]: company2.ccc.receivable_days,
    },
    {
      metric: 'Payable Days',
      [company1.name]: company1.ccc.payable_days,
      [company2.name]: company2.ccc.payable_days,
    },
    {
      metric: 'CCC',
      [company1.name]: company1.ccc.ccc,
      [company2.name]: company2.ccc.ccc,
    },
  ];

  return (
    <div className="chart-container">
      <h3>Company Comparison</h3>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="metric" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={company1.name} fill="#667eea" />
          <Bar dataKey={company2.name} fill="#f093fb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
