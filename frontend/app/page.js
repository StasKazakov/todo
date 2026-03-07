import Chat from "../components/Chat";

export default function Home() {
  return (
    <main className="h-screen flex flex-col items-center justify-center bg-[#222125] overflow-hidden">
      <h1 className="text-5xl font-bold mb-4 mt-20">ToDo LTD Chatbot</h1>
      <Chat />
    </main>
  );
}
