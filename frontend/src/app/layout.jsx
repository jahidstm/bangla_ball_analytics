import { Outfit, Inter } from "next/font/google";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";
import "./globals.css";

const outfit = Outfit({ 
  subsets: ["latin"],
  variable: "--font-heading",
});

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-body",
});

export const metadata = {
  title: "Bangla Ball Analytics",
  description: "AI-powered football insights and content generation",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${outfit.variable} ${inter.variable}`} suppressHydrationWarning>
      <body className="antialiased text-slate-200 flex flex-col h-screen overflow-hidden bg-slate-950" suppressHydrationWarning>
        <Navbar />
        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-6 md:p-8">
            <div className="max-w-5xl mx-auto h-full">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
