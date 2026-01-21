import { Link, NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Upload' },
  { to: '/results/last', label: 'Results' },
  { to: '/quality/last', label: 'Quality' },
  { to: '/triage/last', label: 'Triage' },
  { to: '/risk/last', label: 'Risk' },
  { to: '/reports/last', label: 'Reports' },
  { to: '/history', label: 'History' },
  { to: '/admin', label: 'Admin' }
]

interface NavbarProps {
  onToggleTheme: () => void
  onAbout: () => void
}

export default function Navbar({ onToggleTheme, onAbout }: NavbarProps) {
  return (
    <nav className="sticky top-0 z-10 bg-white/90 backdrop-blur border-b border-slate-200 dark:bg-slate-900/90 dark:border-slate-700">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-lg">Murmur Screen</Link>
        <div className="flex gap-4 text-sm">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `hover:text-blue-600 ${isActive ? 'text-blue-600 font-semibold' : ''}`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-1 border rounded" onClick={onToggleTheme}>
            Theme
          </button>
          <button className="px-3 py-1 border rounded" onClick={onAbout}>
            About
          </button>
        </div>
      </div>
    </nav>
  )
}
