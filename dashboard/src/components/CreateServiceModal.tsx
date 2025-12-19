import { useState, useEffect } from 'react'
import './CreateServiceModal.css'

const API_BASE = 'http://localhost:8000/api/v1'

interface CreateServiceModalProps {
    onClose: () => void
    onSuccess: () => void
}

export default function CreateServiceModal({ onClose, onSuccess }: CreateServiceModalProps) {
    const [name, setName] = useState('')
    const [template, setTemplate] = useState('')
    const [aiEnhance, setAiEnhance] = useState(false)
    const [templates, setTemplates] = useState<string[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    useEffect(() => {
        fetch(`${API_BASE}/services/templates`)
            .then(res => res.json())
            .then(data => {
                setTemplates(data)
                if (data.length > 0) setTemplate(data[0])
            })
            .catch(err => console.error('Failed to fetch templates:', err))
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            const response = await fetch(`${API_BASE}/services/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name,
                    template,
                    ai_enhance: aiEnhance
                })
            })

            if (!response.ok) {
                const data = await response.json()
                throw new Error(data.detail || 'Failed to create service')
            }

            onSuccess()
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Create New Service</h2>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="name">Service Name</label>
                        <input
                            id="name"
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="my-awesome-service"
                            required
                            pattern="[a-z0-9-]+"
                            title="Use lowercase letters, numbers, and hyphens only"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="template">Template</label>
                        <select
                            id="template"
                            value={template}
                            onChange={(e) => setTemplate(e.target.value)}
                            required
                        >
                            {templates.map(t => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group checkbox-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={aiEnhance}
                                onChange={(e) => setAiEnhance(e.target.checked)}
                            />
                            <span>Enable AI Optimization</span>
                        </label>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <div className="modal-actions">
                        <button type="button" className="btn-secondary" onClick={onClose}>
                            Cancel
                        </button>
                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? 'Creating...' : 'Create Service'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
