import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listDocuments as fetchDocuments, listConversations as fetchConversations } from '../api/client';
import { Document, Conversation } from '../types';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [documentsResponse, conversationsResponse] = await Promise.all([
          fetchDocuments(),
          fetchConversations(),
        ]);

        setDocuments(documentsResponse);
        setConversations(conversationsResponse);
      } catch (err) {
        setError('Failed to fetch data. Please try again later.');
        toast.error('Error fetching data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold mb-2">Documents</h2>
              <p className="text-3xl font-bold">{documents.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold mb-2">Conversations</h2>
              <p className="text-3xl font-bold">{conversations.length}</p>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Recent Documents</h2>
            <ul className="bg-white shadow rounded-lg divide-y">
              {documents.slice(0, 5).map((doc) => (
                <li key={doc.id} className="p-4">
                  <p className="font-medium">{doc.name}</p>
                  <p className="text-sm text-gray-500">{doc.uploadedAt}</p>
                </li>
              ))}
              {documents.length === 0 && (
                <li className="p-4 text-gray-500">No documents available.</li>
              )}
            </ul>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Recent Conversations</h2>
            <ul className="bg-white shadow rounded-lg divide-y">
              {conversations.slice(0, 5).map((conv) => (
                <li key={conv.id} className="p-4">
                  <p className="font-medium">Conversation {conv.id}</p>
                  <p className="text-sm text-gray-500">{conv.createdAt}</p>
                </li>
              ))}
              {conversations.length === 0 && (
                <li className="p-4 text-gray-500">No conversations available.</li>
              )}
            </ul>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleUploadClick}
              className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600"
            >
              Upload Document
            </button>
            <button
              onClick={handleChatClick}
              className="bg-green-500 text-white px-4 py-2 rounded shadow hover:bg-green-600"
            >
              Start Chat
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;