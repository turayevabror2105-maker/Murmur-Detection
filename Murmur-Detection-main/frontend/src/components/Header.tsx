import { NavLink } from 'react-router-dom';

export default function Header() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'bg-slate-800 text-emerald-300' : 'text-slate-200 hover:text-white'}`;

  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="text-xl font-bold text-emerald-300">Murmur Screening Demo</div>
        <nav className="flex gap-2">
          <NavLink to="/" className={linkClass}>
            Home
          </NavLink>
          <NavLink to="/upload" className={linkClass}>
            Upload
          </NavLink>
          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>
          <NavLink to="/about" className={linkClass}>
            About
          </NavLink>
          <NavLink to="/privacy" className={linkClass}>
            Privacy
          </NavLink>
          <NavLink to="/terms" className={linkClass}>
            Terms
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
