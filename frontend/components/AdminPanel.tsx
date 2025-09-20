import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Plus, Edit, Trash2, Package, Save, X } from 'lucide-react';
import axios from 'axios';

interface Sweet {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
  description: string;
  image_url?: string;
  created_at: string;
}

interface SweetForm {
  name: string;
  category: string;
  price: string;
  quantity: string;
  description: string;
  image_url: string;
}

const AdminPanel: React.FC = () => {
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingSweet, setEditingSweet] = useState<Sweet | null>(null);
  const [formData, setFormData] = useState<SweetForm>({
    name: '',
    category: '',
    price: '',
    quantity: '',
    description: '',
    image_url: ''
  });
  
  const { token } = useAuth();
  const categories = ['Traditional', 'Bengali', 'Premium', 'South Indian'];

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/sweets', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSweets(response.data);
    } catch (error) {
      console.error('Failed to fetch sweets:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      category: '',
      price: '',
      quantity: '',
      description: '',
      image_url: ''
    });
    setEditingSweet(null);
    setShowForm(false);
  };

  const handleEdit = (sweet: Sweet) => {
    setEditingSweet(sweet);
    setFormData({
      name: sweet.name,
      category: sweet.category,
      price: sweet.price.toString(),
      quantity: sweet.quantity.toString(),
      description: sweet.description,
      image_url: sweet.image_url || ''
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const sweetData = {
      name: formData.name,
      category: formData.category,
      price: parseFloat(formData.price),
      quantity: parseInt(formData.quantity),
      description: formData.description,
      image_url: formData.image_url || null
    };

    try {
      if (editingSweet) {
        // Update existing sweet
        await axios.put(
          `http://localhost:8000/api/sweets/${editingSweet.id}`,
          sweetData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      } else {
        // Create new sweet
        await axios.post(
          'http://localhost:8000/api/sweets',
          sweetData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
      
      await fetchSweets();
      resetForm();
    } catch (error) {
      console.error('Failed to save sweet:', error);
      alert('Failed to save sweet. Please try again.');
    }
  };

  const handleDelete = async (sweetId: number) => {
    if (!confirm('Are you sure you want to delete this sweet?')) return;
    
    try {
      await axios.delete(`http://localhost:8000/api/sweets/${sweetId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchSweets();
    } catch (error) {
      console.error('Failed to delete sweet:', error);
      alert('Failed to delete sweet. Please try again.');
    }
  };

  const handleRestock = async (sweetId: number) => {
    const quantity = prompt('Enter quantity to restock:');
    if (!quantity || isNaN(parseInt(quantity))) return;

    try {
      await axios.post(
        `http://localhost:8000/api/sweets/${sweetId}/restock`,
        { quantity: parseInt(quantity) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      await fetchSweets();
    } catch (error) {
      console.error('Failed to restock sweet:', error);
      alert('Failed to restock sweet. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading admin panel...</p>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Admin Panel</h1>
        <button 
          onClick={() => setShowForm(true)} 
          className="add-btn"
        >
          <Plus size={20} />
          Add New Sweet
        </button>
      </div>

      {/* Add/Edit Form Modal */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>{editingSweet ? 'Edit Sweet' : 'Add New Sweet'}</h2>
              <button onClick={resetForm} className="close-btn">
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="sweet-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required
                    className="form-input"
                  />
                </div>
                
                <div className="form-group">
                  <label>Category *</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                    required
                    className="form-input"
                  >
                    <option value="">Select Category</option>
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Price (₹) *</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData({...formData, price: e.target.value})}
                    required
                    className="form-input"
                  />
                </div>
                
                <div className="form-group">
                  <label>Quantity *</label>
                  <input
                    type="number"
                    value={formData.quantity}
                    onChange={(e) => setFormData({...formData, quantity: e.target.value})}
                    required
                    className="form-input"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Description *</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required
                  className="form-textarea"
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Image URL</label>
                <input
                  type="url"
                  value={formData.image_url}
                  onChange={(e) => setFormData({...formData, image_url: e.target.value})}
                  className="form-input"
                  placeholder="https://example.com/image.jpg"
                />
              </div>

              <div className="form-actions">
                <button type="button" onClick={resetForm} className="cancel-btn">
                  Cancel
                </button>
                <button type="submit" className="save-btn">
                  <Save size={16} />
                  {editingSweet ? 'Update' : 'Create'} Sweet
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sweets Table */}
      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sweets.map(sweet => (
              <tr key={sweet.id}>
                <td>
                  <img 
                    src={sweet.image_url || '/api/placeholder/60/60'} 
                    alt={sweet.name}
                    className="table-image"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = '/api/placeholder/60/60';
                    }}
                  />
                </td>
                <td>
                  <div className="sweet-name-cell">
                    <strong>{sweet.name}</strong>
                    <small>{sweet.description}</small>
                  </div>
                </td>
                <td>
                  <span className="category-badge">{sweet.category}</span>
                </td>
                <td>₹{sweet.price}</td>
                <td>
                  <span className={`quantity ${sweet.quantity === 0 ? 'zero' : sweet.quantity < 10 ? 'low' : ''}`}>
                    {sweet.quantity}
                  </span>
                </td>
                <td>
                  <span className={`status ${sweet.quantity > 0 ? 'in-stock' : 'out-of-stock'}`}>
                    {sweet.quantity > 0 ? 'In Stock' : 'Out of Stock'}
                  </span>
                </td>
                <td>
                  <div className="action-buttons">
                    <button
                      onClick={() => handleEdit(sweet)}
                      className="edit-btn"
                      title="Edit"
                    >
                      <Edit size={16} />
                    </button>
                    <button
                      onClick={() => handleRestock(sweet.id)}
                      className="restock-btn"
                      title="Restock"
                    >
                      <Package size={16} />
                    </button>
                    <button
                      onClick={() => handleDelete(sweet.id)}
                      className="delete-btn"
                      title="Delete"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {sweets.length === 0 && (
          <div className="no-data">
            <p>No sweets found. Add your first sweet to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;