import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "ToDo LTD Chatbot",
  description: "The best chatbot in the world!",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Toaster position="top-center"
         reverseOrder={false} 
         toastOptions={{
            duration: 4000,      
            style: {
              background: "#000000",  
              color: "#ffffff",       
              fontWeight: 500,
              fontSize: "14px",
            },
          }}/>
      </body>
    </html>
  );
}
