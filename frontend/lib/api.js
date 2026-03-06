export async function sendMessage(message) {
  const res = await fetch("http://localhost:8000/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: message }),
  });
  return res.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/api/upload", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Error uploading file");

  return res.json(); 
}