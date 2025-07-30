import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-8">Designer</h1>
        <div className="bg-gray-800 p-8 rounded-lg">
          <button
            onClick={() => setCount(count => count + 1)}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-medium transition-colors mb-4"
          >
            count is {count}
          </button>
          <p className="text-gray-300">
            Edit{' '}
            <code className="bg-gray-700 px-2 py-1 rounded">src/App.tsx</code>{' '}
            and save to test HMR
          </p>
        </div>
        <p className="text-gray-400 mt-4">
          Click on the button to test the counter
        </p>
      </div>
    </div>
  )
}

export default App
