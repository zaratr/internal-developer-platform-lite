import type { Service } from '../App'
import './ServiceList.css'

interface ServiceListProps {
    services: Service[]
}

export default function ServiceList({ services }: ServiceListProps) {
    if (services.length === 0) {
        return (
            <div className="empty-state">
                <h2>No services yet</h2>
                <p>Create your first service to get started</p>
            </div>
        )
    }

    return (
        <div className="service-grid">
            {services.map((service) => (
                <div key={service.name} className="service-card">
                    <div className="service-header">
                        <h3>{service.name}</h3>
                        <span className={`status-badge ${service.status.toLowerCase()}`}>
                            {service.status}
                        </span>
                    </div>
                    <div className="service-details">
                        {service.template && (
                            <div className="detail-row">
                                <span className="label">Template:</span>
                                <span className="value">{service.template}</span>
                            </div>
                        )}
                        <div className="detail-row">
                            <span className="label">Path:</span>
                            <span className="value path">{service.path}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
