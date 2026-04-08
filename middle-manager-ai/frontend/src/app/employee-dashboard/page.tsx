"use client";

import { useState } from 'react';

export default function EmployeeDashboard() {
  const [request, setRequest] = useState('');
  const [response, setResponse] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: request })
      });
      const data = await res.json();
      setResponse(data.responses);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Grassroots (IC) Dashboard</h1>
        
        <div className="bg-white p-6 rounded-lg shadow-sm mb-8 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Request Support from Middle-Manager AI</h2>
          <form onSubmit={handleSubmit}>
            <textarea 
              className="w-full p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 text-black"
              rows={4}
              placeholder="E.g., I need to take a leave next Friday, or I am blocked by the design team..."
              value={request}
              onChange={(e) => setRequest(e.target.value)}
            />
            <button 
              type="submit" 
              disabled={loading}
              className="mt-4 bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 transition-colors"
            >
              {loading ? 'Sending to Middle-Manager AI...' : 'Send Request'}
            </button>
          </form>
        </div>

        {response.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 text-blue-700">AI Response</h2>
            <div className="space-y-4">
              {response.map((res, i) => (
                <div key={i} className="p-4 bg-gray-50 rounded border border-gray-100 text-gray-800">
                  {res}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
