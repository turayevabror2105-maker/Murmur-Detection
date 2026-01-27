import React from 'react'

export interface ToastMessage {
  id: string
  type: 'success' | 'error'
  message: string
}

interface ToastProps {
  messages: ToastMessage[]
  onDismiss: (id: string) => void
}

export default function Toast({ messages, onDismiss }: ToastProps) {
  return (
    <div className="fixed top-20 right-4 space-y-2 z-50">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`px-4 py-2 rounded shadow text-white ${
            msg.type === 'success' ? 'bg-emerald-500' : 'bg-rose-500'
          }`}
        >
          <div className="flex items-center gap-2">
            <span>{msg.message}</span>
            <button onClick={() => onDismiss(msg.id)} className="text-white">✕</button>
          </div>
        </div>
      ))}
    </div>
  )
}
