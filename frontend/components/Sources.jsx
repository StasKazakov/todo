export default function Sources({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2 p-2 bg-gray-50 border rounded-md">
      <p className="font-bold mb-1">Sources:</p>
      <ul className="list-disc list-inside text-sm">
        {sources.map((s, idx) => (
          <li key={idx}>
            Page {s.page}: {s.text.substring(0, 60)}...
          </li>
        ))}
      </ul>
    </div>
  );
}