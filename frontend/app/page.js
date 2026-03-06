import Chat from "../components/Chat";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#222125]">
      <h1 className="text-5xl font-bold mb-4">ToDo LTD Chatbot</h1>
      <Chat />
    </main>
  );
}
