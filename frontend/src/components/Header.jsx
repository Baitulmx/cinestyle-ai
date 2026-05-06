export default function Header({ onReset }) {
  return (
    <header className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 shadow-lg">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="flex justify-between items-center">
          <div className="cursor-pointer group" onClick={onReset}>
            <div className="flex items-center gap-3">
              <div className="text-4xl">✨</div>
              <div>
                <h1 className="text-4xl font-bold text-white group-hover:scale-105 transition transform">CineStyle AI</h1>
                <p className="text-sm text-indigo-100">AI-Powered Outfit Recommendations</p>
              </div>
            </div>
            <p className="text-xs text-indigo-200 mt-1 group-hover:text-white transition">Inspired by Film & TV Characters</p>
          </div>
          <div className="text-right hidden md:block">
            <p className="text-sm text-indigo-100">🎬 Discover Your Style 🎬</p>
          </div>
        </div>
      </div>
    </header>
  )
}
