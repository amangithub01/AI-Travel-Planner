"use client";
import React, { useState } from 'react';
import { Plane, Hotel, Cloud, Calendar, MapPin, Search, Loader2, Navigation, Utensils, Info, Camera, Sparkles, Printer } from 'lucide-react';
import { planTrip } from '../lib/api';

const AIRPORTS = [
  "Mumbai (BOM)", "Delhi (DEL)", "Hyderabad (HYD)", "Bengaluru (BLR)", "Chennai (MAA)", "Kolkata (CCU)",
  "Dubai (DXB)", "New York (JFK)", "London (LHR)", "Paris (CDG)", "Tokyo (HND)", "Singapore (SIN)"
];

const flightTimes = [
  { dep: "06:15 AM", arr: "08:30 AM" },
  { dep: "10:45 AM", arr: "01:00 PM" },
  { dep: "04:20 PM", arr: "06:35 PM" }
];

const hotelImages = [
  "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=150&q=80",
  "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?auto=format&fit=crop&w=150&q=80"
];

export default function TravelDashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    start_date: '2026-05-10',
    end_date: '2026-05-15',
    max_price: 5000
  });

  const extractCode = (text: string) => {
    const match = text.match(/\(([A-Z]{3})\)/);
    return match ? match[1] : text.trim();
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const data = await planTrip({
        ...formData,
        origin: extractCode(formData.origin),
        destination: extractCode(formData.destination)
      });
      setResult(data);
    } catch (err) {
      alert("Error: Ensure your Python backend is running!");
    } finally {
      setLoading(false);
    }
  };

  const cleanText = (text: string) => text.replace(/\*/g, '').replace(/#/g, '').trim();

  const parseItinerary = (text: string) => {
    if (!text) return [];
    return text.split(/#{3,4}\sDay\s\d+/i).filter(d => d.trim().length > 10);
  };

  // Triggers the native browser print/save as PDF dialog
  const handlePrint = () => {
    window.print();
  };

  return (
    // Added print:bg-white to ensure the PDF background is clean
    <div className="min-h-screen bg-[#F8FAFC] print:bg-white font-sans text-slate-900 selection:bg-blue-500/30 flex flex-col">

      {/* 1. HERO SECTION (Hidden during PDF export to save space/ink) */}
      <div
        className="relative w-full pt-6 pb-32 flex flex-col items-center print:hidden"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2074&auto=format&fit=crop')",
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/80 via-slate-900/50 to-[#F8FAFC]"></div>

        <nav className="relative z-10 w-full px-6 flex justify-between items-center max-w-7xl mx-auto mb-16">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-xl shadow-lg shadow-blue-500/30">
              <Plane className="text-white w-6 h-6" />
            </div>
            <h1 className="text-2xl font-black tracking-tight text-white">AI Travel Planner</h1>
          </div>
        </nav>

        <div className="relative z-10 text-center px-4 max-w-3xl">
          <h2 className="text-4xl md:text-6xl font-black text-white mb-6 drop-shadow-lg leading-tight">Design Your Perfect Journey</h2>
          <p className="text-blue-100 text-lg font-medium drop-shadow-md">Smart itineraries, live weather, and curated stays powered by AI agents.</p>
        </div>
      </div>

      {/* 2. SEARCH BOX (Hidden during PDF export) */}
      <div className="flex-grow px-4 md:px-10 relative z-20 -mt-20 print:hidden">
        <form onSubmit={handleSearch} className="max-w-7xl mx-auto bg-white p-6 md:p-8 rounded-[2rem] shadow-2xl shadow-blue-900/10 border border-slate-100 mb-12 grid grid-cols-1 md:grid-cols-6 gap-6 items-end">

          <datalist id="airport-list">
            {AIRPORTS.map(airport => <option key={airport} value={airport} />)}
          </datalist>

          <div className="md:col-span-1">
            <label className="text-[10px] font-black uppercase text-blue-600 mb-2 block ml-1">From</label>
            <div className="relative group">
              <MapPin className="absolute left-3 top-3.5 w-4 h-4 text-slate-400 group-focus-within:text-blue-600 transition-colors" />
              <input type="text" list="airport-list" placeholder="Mumbai (BOM)" value={formData.origin} onChange={e => setFormData({ ...formData, origin: e.target.value })} required className="w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-transparent focus:border-blue-200 rounded-2xl focus:bg-white transition-all outline-none font-bold text-slate-700" />
            </div>
          </div>
          <div className="md:col-span-1">
            <label className="text-[10px] font-black uppercase text-blue-600 mb-2 block ml-1">To</label>
            <div className="relative group">
              <Search className="absolute left-3 top-3.5 w-4 h-4 text-slate-400 group-focus-within:text-blue-600 transition-colors" />
              <input type="text" list="airport-list" placeholder="Dubai (DXB)" value={formData.destination} onChange={e => setFormData({ ...formData, destination: e.target.value })} required className="w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-transparent focus:border-blue-200 rounded-2xl focus:bg-white transition-all outline-none font-bold text-slate-700" />
            </div>
          </div>
          <div className="md:col-span-1">
            <label className="text-[10px] font-black uppercase text-blue-600 mb-2 block ml-1">Departure</label>
            <div className="relative group">
              <Calendar className="absolute left-3 top-3.5 w-4 h-4 text-slate-400" />
              <input type="date" value={formData.start_date} onChange={e => setFormData({ ...formData, start_date: e.target.value })} required className="w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-transparent focus:border-blue-200 rounded-2xl focus:bg-white transition-all outline-none font-bold text-slate-700 text-sm" />
            </div>
          </div>
          <div className="md:col-span-1">
            <label className="text-[10px] font-black uppercase text-blue-600 mb-2 block ml-1">Return</label>
            <div className="relative group">
              <Calendar className="absolute left-3 top-3.5 w-4 h-4 text-slate-400" />
              <input type="date" value={formData.end_date} onChange={e => setFormData({ ...formData, end_date: e.target.value })} required className="w-full pl-10 pr-4 py-3 bg-slate-50 border-2 border-transparent focus:border-blue-200 rounded-2xl focus:bg-white transition-all outline-none font-bold text-slate-700 text-sm" />
            </div>
          </div>
          <div className="md:col-span-1">
            <label className="text-[10px] font-black uppercase text-blue-600 mb-2 block ml-1">Budget ($ USD)</label>
            <div className="relative group">
              {/* The Dollar Symbol */}
              <span className="absolute left-4 top-3.5 font-black text-slate-400 group-focus-within:text-blue-600 transition-colors">$</span>

              <input
                type="number"
                placeholder="5000"
                value={formData.max_price}
                onChange={e => setFormData({ ...formData, max_price: Number(e.target.value) })}
                required
                className="w-full pl-8 pr-4 py-3 bg-slate-50 border-2 border-transparent focus:border-blue-200 rounded-2xl focus:bg-white transition-all outline-none font-black text-blue-600"
              />
            </div>
          </div>
          <button disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-black py-3 rounded-2xl shadow-xl shadow-blue-600/30 hover:-translate-y-1 transition-all flex items-center justify-center gap-2 h-[52px] disabled:opacity-50">
            {loading ? <Loader2 className="animate-spin w-6 h-6" /> : "Plan Trip"}
          </button>
        </form>

        {/* 3. RESULTS SECTION */}
        {result && (
          // Added print:flex print:flex-col so the PDF flows neatly downwards
          <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 pb-20 animate-in fade-in slide-in-from-bottom-6 duration-1000 print:flex print:flex-col print:pt-10">

            {/* LEFT: VISUAL TIMELINE */}
            <div className="lg:col-span-8 space-y-8 print:w-full">

              {/* HEADER & NEW PRINT BUTTON */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div className="flex items-center gap-4">
                  <Navigation className="text-blue-600 w-8 h-8 print:text-black" />
                  <h2 className="text-3xl font-black text-slate-800 tracking-tight">
                    {extractCode(formData.destination)} Itinerary
                  </h2>
                </div>
                {/* The Print Button - hides itself when printing! */}
                <button
                  onClick={handlePrint}
                  className="print:hidden flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-white px-5 py-2.5 rounded-xl font-bold shadow-md hover:shadow-lg transition-all active:scale-95"
                >
                  <Printer className="w-4 h-4" /> Save as PDF
                </button>
              </div>

              <div className="relative border-l-4 border-blue-200 print:border-slate-300 ml-6 pl-10 space-y-12">
                {parseItinerary(result.itinerary).map((content, index) => {
                  const lines = content.trim().split('\n');
                  const dayTitle = cleanText(lines[0]);
                  const dayBody = cleanText(lines.slice(1).join('\n'));

                  return (
                    // Added print:break-inside-avoid so a day doesn't get cut in half across two pages
                    <div key={index} className="relative group print:break-inside-avoid">
                      <div className="absolute -left-[3.4rem] top-0 w-12 h-12 bg-blue-600 print:bg-slate-800 print:border-slate-200 rounded-full border-4 border-white flex items-center justify-center shadow-lg group-hover:scale-110 transition-all duration-300 z-10">
                        <span className="text-white font-black text-sm">{index + 1}</span>
                      </div>

                      <div className="bg-white p-8 rounded-[2rem] shadow-sm border border-slate-100 print:border-slate-300 print:shadow-none hover:-translate-y-2 hover:scale-[1.02] hover:shadow-2xl hover:shadow-blue-900/10 transition-all duration-300">
                        <h3 className="text-xl font-black text-slate-800 mb-4 flex items-center gap-2">
                          Day {index + 1} <span className="text-slate-300 font-medium">|</span> {dayTitle}
                        </h3>
                        <div className="prose prose-slate max-w-none text-slate-600 leading-relaxed whitespace-pre-wrap font-medium">
                          {dayBody}
                        </div>

                        {index % 2 === 1 && result.food && result.food[index] && (
                          <div className="mt-6 flex items-center gap-4 bg-orange-50/80 print:bg-slate-50 p-4 rounded-2xl border border-orange-100 print:border-slate-200">
                            <div className="bg-orange-100 print:bg-slate-200 p-3 rounded-xl"><Utensils className="w-5 h-5 text-orange-600 print:text-slate-700" /></div>
                            <div>
                              <p className="text-[10px] font-black text-orange-600 print:text-slate-500 uppercase tracking-widest">Local Eats</p>
                              <p className="font-bold text-slate-800">{result.food[index].name}</p>
                            </div>
                          </div>
                        )}

                        {index % 2 === 0 && result.attractions && result.attractions[index] && (
                          <div className="mt-6 flex items-center gap-4 bg-purple-50/80 print:bg-slate-50 p-4 rounded-2xl border border-purple-100 print:border-slate-200">
                            <div className="bg-purple-100 print:bg-slate-200 p-3 rounded-xl"><Camera className="w-5 h-5 text-purple-600 print:text-slate-700" /></div>
                            <div>
                              <p className="text-[10px] font-black text-purple-600 print:text-slate-500 uppercase tracking-widest">Must See</p>
                              <p className="font-bold text-slate-800">{result.attractions[index].name}</p>
                            </div>
                          </div>
                        )}

                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* RIGHT: SMART INFO SIDEBAR */}
            <div className="lg:col-span-4 space-y-8 sticky top-10 h-fit print:static print:w-full">

              <div className="bg-gradient-to-br from-blue-500 to-blue-600 print:from-slate-100 print:to-slate-100 text-white print:text-slate-800 p-10 rounded-[2.5rem] shadow-2xl shadow-blue-500/30 print:shadow-none print:border print:border-slate-300 relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300 print:break-inside-avoid">
                <Cloud className="absolute -right-4 -top-4 w-32 h-32 opacity-20 print:opacity-5 group-hover:scale-110 group-hover:rotate-12 transition-all duration-700 print:text-black" />
                <h3 className="text-xs font-black uppercase tracking-[0.2em] mb-4 opacity-80 flex items-center gap-2"><Cloud className="w-4 h-4" /> Destination Forecast</h3>
                <p className="text-4xl lg:text-5xl font-black">{result.weather}</p>
              </div>

              {/* UPGRADED FLIGHTS */}
              <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 print:border-slate-300 print:shadow-none hover:shadow-xl transition-all duration-300 print:break-inside-avoid">
                <h3 className="text-lg font-black flex items-center gap-2 mb-6 text-slate-800"><Plane className="text-orange-500 print:text-slate-800 w-5 h-5" /> Top Flight Options</h3>
                <div className="space-y-4">
                  {result.flights && result.flights.length > 0 ? (
                    result.flights.slice(0, 3).map((f: any, i: number) => (
                      <div key={i} className="relative p-5 bg-white rounded-2xl border border-slate-100 print:border-slate-200 shadow-sm print:shadow-none hover:border-orange-200 transition-all">

                        {i === 0 && (
                          <div className="absolute -top-3 -right-2 bg-emerald-500 print:bg-slate-800 text-white text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full shadow-lg print:shadow-none flex items-center gap-1">
                            <Sparkles className="w-3 h-3" /> Best Value
                          </div>
                        )}

                        <div className="flex justify-between items-center mb-4">
                          <div className="flex items-center gap-3">
                            <img src={`https://ui-avatars.com/api/?name=${f.airline}&background=f1f5f9&color=0f172a&rounded=true&bold=true`} alt={f.airline} className="w-8 h-8 rounded-full shadow-sm" />
                            <span className="font-extrabold text-slate-800">{f.airline}</span>
                          </div>
                          <span className="text-orange-600 print:text-slate-800 font-black text-xl">${f.price}</span>
                        </div>

                        <div className="flex items-center justify-between text-xs font-bold text-slate-400">
                          <span>{flightTimes[i % 3].dep}</span>
                          <div className="flex-1 flex items-center px-3">
                            <div className="h-[2px] w-full bg-slate-200 border-dashed border-t-2 border-slate-300"></div>
                            <Plane className="w-4 h-4 mx-2 text-slate-300 rotate-45 flex-shrink-0" />
                            <div className="h-[2px] w-full bg-slate-200 border-dashed border-t-2 border-slate-300"></div>
                          </div>
                          <span>{flightTimes[i % 3].arr}</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 text-sm font-medium">No flights found for this route.</p>
                  )}
                </div>
              </div>

              {/* UPGRADED HOTELS */}
              <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100 print:border-slate-300 print:shadow-none hover:shadow-xl transition-all duration-300 print:break-inside-avoid">
                <h3 className="text-lg font-black flex items-center gap-2 mb-6 text-slate-800"><Hotel className="text-emerald-500 print:text-slate-800 w-5 h-5" /> Curated Stays</h3>
                <div className="space-y-4">
                  {result.hotels && result.hotels.length > 0 ? (
                    result.hotels.slice(0, 3).map((h: any, i: number) => (
                      <div key={i} className="relative p-4 bg-white rounded-2xl border border-slate-100 print:border-slate-200 shadow-sm print:shadow-none flex items-center gap-4">

                        {i === 0 && (
                          <div className="absolute -top-3 -right-2 bg-orange-500 print:bg-slate-800 text-white text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full shadow-lg print:shadow-none">
                            Top Pick
                          </div>
                        )}

                        <img src={hotelImages[i % 3]} alt="Hotel" className="w-16 h-16 rounded-xl object-cover shadow-sm" />

                        <div className="flex-1 min-w-0">
                          <div className="flex justify-between items-start mb-1">
                            <span className="font-bold text-slate-800 truncate pr-2">{h.name}</span>
                          </div>
                          <div className="flex items-center justify-between mt-2">
                            <div className="flex items-center gap-1 bg-amber-50 print:bg-slate-100 px-2 py-0.5 rounded-md">
                              <span className="text-[10px] font-bold text-amber-600 print:text-slate-600">
                                {h.rating && h.rating > 0 ? `${h.rating} ★` : 'New / Unrated'}
                              </span>
                            </div>
                            <span className="text-emerald-600 print:text-slate-800 font-black text-lg">${h.price}<span className="text-[10px] text-slate-400 font-medium">/nt</span></span>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 text-sm font-medium">No hotels found.</p>
                  )}
                </div>
              </div>

            </div>
          </div>
        )}
      </div>
    </div>
  );
}