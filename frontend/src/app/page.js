"use client";
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, ArrowRight, Rocket, Shield, Sparkles, FileText, CheckCircle2, 
  Settings, Key, Info, UploadCloud, Users, Eye, EyeOff, HelpCircle, 
  ChevronRight, FileSignature, Target, PieChart, Layers, Network, UserRound, Plus, Search, Bell, LayoutDashboard
} from 'lucide-react';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] }
};

const stagger = {
  animate: { transition: { staggerChildren: 0.1 } }
};

export default function LandingPage() {
  const [showApi, setShowApi] = useState(false);
  const [resumeFiles, setResumeFiles] = useState([
    { name: "Shreya_Chauhan.pdf", size: "40.1KB" }
  ]);

  const removeFile = (name) => {
    setResumeFiles(resumeFiles.filter(f => f.name !== name));
  };

  return (
    <div className="min-h-screen bg-[#0a0a14] text-slate-200 selection:bg-violet-500/30 selection:text-violet-200 relative overflow-x-hidden">
      
      {/* Ambient Background Glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-[-20%] left-[10%] w-[600px] h-[600px] bg-violet-600/10 rounded-full blur-[120px] opacity-60"></div>
        <div className="absolute bottom-[-10%] right-[5%] w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[100px] opacity-40"></div>
      </div>

      {/* 1) STICKY NAVBAR */}
      <nav className="sticky top-0 z-50 border-b border-white/[0.06] bg-[#0a0a14]/70 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          
          {/* Left: Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(124,58,237,0.4)]">
              <Brain size={18} className="text-white" />
            </div>
            <span className="font-bold tracking-tight text-white font-['Space_Grotesk'] text-lg">NexHire AI</span>
          </div>

          {/* Center: Links */}
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-white transition-colors">How It Works</a>
            <a href="#" className="hover:text-white transition-colors">Pricing</a>
            <a href="#" className="hover:text-white transition-colors">Docs</a>
            <a href="#" className="hover:text-white transition-colors">FAQ</a>
          </div>

          {/* Right: CTAs */}
          <div className="flex items-center gap-6">
            <a href="#" className="hidden sm:block text-xs font-semibold tracking-wider text-slate-400 hover:text-white transition-colors uppercase">API Docs</a>
            <a href="#" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">Sign in</a>
            <button className="px-4 py-2 rounded-[10px] bg-gradient-to-r from-violet-600 via-fuchsia-600 to-violet-600 bg-[length:200%_auto] hover:bg-right text-white font-semibold text-sm transition-all duration-300 shadow-[0_0_20px_rgba(124,58,237,0.3)] hover:shadow-[0_0_25px_rgba(124,58,237,0.5)] active:scale-[0.98]">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      <main className="relative z-10">
        
        {/* 2) HERO SECTION */}
        <section className="relative pt-24 pb-32 overflow-hidden">
          <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-16 items-center">
            
            {/* Hero Left */}
            <div className="lg:col-span-6 space-y-8">
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
                className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-violet-500/20 bg-violet-500/5 text-violet-400 text-xs font-semibold tracking-wide"
              >
                <Sparkles size={12} /> ✨ Powered by Google Gemini & LangGraph
              </motion.div>

              <motion.h1 
                variants={fadeInUp} initial="initial" animate="animate"
                className="text-5xl sm:text-6xl lg:text-7xl font-extrabold font-['Space_Grotesk'] tracking-tight leading-[1.1] text-white"
              >
                AI-Powered <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-fuchsia-400 to-indigo-400">Screening.</span><br />
                Smarter <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-violet-400 to-fuchsia-400">Hiring.</span>
              </motion.h1>

              <motion.p 
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
                className="text-lg text-slate-400 font-normal leading-relaxed max-w-lg"
              >
                NexHire AI is a modern agentic screening system that evaluates candidates against custom job requirements using deep semantic analysis and a 5-dimension rubric.
              </motion.p>

              <motion.div 
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
                className="flex flex-wrap gap-4 pt-2"
              >
                <button className="flex items-center gap-2 px-6 py-3.5 rounded-[10px] bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-bold shadow-lg shadow-violet-600/25 hover:shadow-violet-600/40 transition-all hover:-translate-y-[2px]">
                  Get Started Free <Rocket size={16} />
                </button>
                <button className="flex items-center gap-2 px-6 py-3.5 rounded-[10px] border border-white/10 bg-white/[0.02] text-white font-semibold hover:bg-white/[0.05] hover:border-white/20 transition-all">
                  View Documentation
                </button>
              </motion.div>

              <motion.div 
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
                className="flex flex-wrap items-center gap-x-6 gap-y-2 pt-4 text-xs font-medium text-slate-500"
              >
                <div className="flex items-center gap-1.5"><Shield size={14} /> No Credit Card Required</div>
                <span className="w-1 h-1 bg-slate-700 rounded-full hidden sm:block"></span>
                <div className="flex items-center gap-1.5"><CheckCircle2 size={14} /> Secure & Private</div>
                <span className="w-1 h-1 bg-slate-700 rounded-full hidden sm:block"></span>
                <div className="flex items-center gap-1.5"><Layers size={14} /> Cancel Anytime</div>
              </motion.div>
            </div>

            {/* Hero Right: Realistic Dashboard Mockup */}
            <div className="lg:col-span-6 relative group">
              {/* Glow Behind Card */}
              <div className="absolute inset-0 bg-gradient-to-tr from-violet-600/20 to-fuchsia-600/20 rounded-2xl blur-3xl -z-10 opacity-60 group-hover:opacity-80 transition-opacity duration-700"></div>
              
              <motion.div 
                initial={{ opacity: 0, rotateX: 5, y: 30 }}
                animate={{ opacity: 1, rotateX: 0, y: 0 }}
                transition={{ duration: 0.8, delay: 0.1 }}
                className="relative rounded-2xl border border-white/10 bg-[#0e0e18] shadow-2xl overflow-hidden aspect-[4/3] flex text-[12px]"
              >
                {/* Sidebar Mock */}
                <div className="w-48 h-full border-r border-white/5 bg-[#0c0c12] p-4 flex flex-col gap-6">
                  <div className="flex items-center gap-2 px-2">
                    <div className="w-5 h-5 rounded bg-violet-600 flex items-center justify-center text-[10px] font-bold text-white">H</div>
                    <span className="font-semibold text-white text-[13px]">NexHire</span>
                  </div>
                  <div className="space-y-1 text-slate-400">
                    <div className="flex items-center gap-2 px-2 py-1.5 bg-white/5 text-white rounded-md"><LayoutDashboard size={14} /> Overview</div>
                    <div className="flex items-center gap-2 px-2 py-1.5 hover:text-white transition-colors"><FileText size={14} /> Submissions</div>
                    <div className="flex items-center gap-2 px-2 py-1.5 hover:text-white transition-colors"><Users size={14} /> Talent Pool</div>
                    <div className="flex items-center gap-2 px-2 py-1.5 hover:text-white transition-colors"><PieChart size={14} /> Analytics</div>
                  </div>
                  <div className="mt-auto flex items-center gap-2 px-2 text-slate-400 py-1.5 hover:text-white"><Settings size={14} /> Settings</div>
                </div>

                {/* Main Body Mock */}
                <div className="flex-1 bg-[#0a0a10] overflow-y-auto">
                  {/* Top Nav Mock */}
                  <div className="h-12 border-b border-white/5 flex items-center justify-between px-6">
                    <div className="flex items-center gap-2 text-slate-400"><Search size={14} /> <span>Search...</span></div>
                    <div className="flex items-center gap-3 text-slate-400"><Bell size={14} /><div className="w-6 h-6 rounded-full bg-violet-600/40 border border-violet-500/50"></div></div>
                  </div>

                  <div className="p-6 space-y-6">
                    <h3 className="text-base font-bold text-white">Welcome back! 👋</h3>

                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-3">
                      <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-3">
                        <div className="text-slate-500 font-medium mb-1">Total Submissions</div>
                        <div className="flex items-baseline justify-between">
                          <span className="text-xl font-bold text-white">128</span>
                          <span className="text-[10px] text-emerald-400 font-bold">+23%</span>
                        </div>
                      </div>
                      <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-3">
                        <div className="text-slate-500 font-medium mb-1">Screenings</div>
                        <div className="flex items-baseline justify-between">
                          <span className="text-xl font-bold text-white">96</span>
                          <span className="text-[10px] text-emerald-400 font-bold">+18%</span>
                        </div>
                      </div>
                      <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-3">
                        <div className="text-slate-500 font-medium mb-1">Top Candidates</div>
                        <div className="flex items-baseline justify-between">
                          <span className="text-xl font-bold text-white">24</span>
                          <span className="text-[10px] text-emerald-400 font-bold">+12%</span>
                        </div>
                      </div>
                    </div>

                    {/* Table Mock */}
                    <div className="space-y-3">
                      <h4 className="text-[13px] font-semibold text-white">Recent Submissions</h4>
                      <div className="bg-white/[0.01] border border-white/5 rounded-xl divide-y divide-white/5 overflow-hidden">
                        {[
                          { name: "Arjun Patel", role: "Frontend Eng.", score: 92, match: "High Match", c: "emerald" },
                          { name: "Sarah Johnson", role: "Backend Dev", score: 88, match: "High Match", c: "emerald" },
                          { name: "Rahul Verma", role: "UX Researcher", score: 79, match: "Good Match", c: "violet" },
                          { name: "Priya Sharma", role: "Data Scientist", score: 84, match: "High Match", c: "emerald" }
                        ].map((row, i) => (
                          <div key={i} className="px-4 py-2.5 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
                            <div className="flex items-center gap-3">
                              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-slate-800 to-slate-700 border border-white/10 flex items-center justify-center text-[10px] font-medium">{row.name[0]}</div>
                              <div>
                                <div className="font-medium text-slate-200">{row.name}</div>
                                <div className="text-[10px] text-slate-500">{row.role}</div>
                              </div>
                            </div>
                            <div className="flex items-center gap-4">
                              <div className="font-bold text-slate-300">{row.score}/100</div>
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${row.c === 'emerald' ? 'text-emerald-400 bg-emerald-400/10 border border-emerald-400/20' : 'text-violet-400 bg-violet-400/10 border border-violet-400/20'}`}>{row.match}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>
                </div>
              </motion.div>
            </div>

          </div>
        </section>

        {/* 3) FEATURES STRIP */}
        <section id="features" className="py-20 relative border-y border-white/[0.05] bg-white/[0.01]">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              
              {[
                { icon: <Target className="text-violet-400" />, title: "Deep Semantic Evaluation", text: "AI agents evaluate candidates across 5 key dimensions using advanced semantic understanding." },
                { icon: <FileSignature className="text-fuchsia-400" />, title: "Custom Rubric", text: "Define your own evaluation rubric tailored to your role and company specific goals." },
                { icon: <Network className="text-violet-400" />, title: "Intelligent Talent Pool", text: "Indexed and searchable talent pool that learns and improves natively over time." },
                { icon: <PieChart className="text-fuchsia-400" />, title: "Actionable Insights", text: "Get clear scores, feedback, and transparent rankings to make hire decisions." },
              ].map((feat, i) => (
                <div key={i} className="group space-y-4">
                  <div className="w-10 h-10 rounded-xl border border-white/10 bg-white/[0.02] flex items-center justify-center transition-all group-hover:border-violet-500/30 group-hover:bg-violet-500/5 shadow-sm">
                    {feat.icon}
                  </div>
                  <h4 className="text-lg font-bold text-white font-['Space_Grotesk']">{feat.title}</h4>
                  <p className="text-sm text-slate-400 leading-relaxed">{feat.text}</p>
                </div>
              ))}

            </div>
          </div>
        </section>

        {/* 4) HOW IT WORKS */}
        <section id="how-it-works" className="py-32 relative">
          <div className="max-w-7xl mx-auto px-6 text-center mb-20">
            <h2 className="text-4xl font-extrabold font-['Space_Grotesk'] text-white tracking-tight mb-4">Intelligent Workflow</h2>
            <p className="text-slate-400 text-lg max-w-xl mx-auto">Our seamless agentic loop optimizes every step from drop to decision.</p>
          </div>

          <div className="max-w-7xl mx-auto px-6 relative">
            {/* Connecting Dotted Line (Desktop Only) */}
            <div className="absolute top-10 left-12 right-12 h-[1px] border-t-2 border-dashed border-white/10 hidden lg:block -z-10"></div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
              {[
                { n: "01", t: "Upload", d: "Upload job description, resumes, and LinkedIn data profile sets." },
                { n: "02", t: "AI Analyze", d: "Our autonomous AI agents analyze and evaluate each candidate context." },
                { n: "03", t: "Rank & Score", d: "Every candidate is ranked with weighted scores and rigorous feedback." },
                { n: "04", t: "Hire Confidently", d: "Review detailed insights dashboard and pull the trigger faster." },
              ].map((step, idx) => (
                <div key={idx} className="relative text-center space-y-4 group">
                  <div className="w-20 h-20 rounded-2xl bg-[#0a0a14] border-2 border-white/10 mx-auto flex items-center justify-center text-2xl font-bold text-white font-['Space_Grotesk'] shadow-[0_0_30px_rgba(0,0,0,0.5)] group-hover:border-violet-500/50 transition-colors duration-500">
                    <span className="bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40">{step.n}</span>
                  </div>
                  <h4 className="text-xl font-bold text-white">{step.t}</h4>
                  <p className="text-slate-400 text-sm leading-relaxed px-4">{step.d}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 5) LIVE APP / "TRY IT" SECTION */}
        <section className="py-32 relative">
          <div className="max-w-7xl mx-auto px-6">
            <div className="bg-[#0d0d17] border border-white/[0.08] rounded-[24px] overflow-hidden shadow-2xl grid grid-cols-1 lg:grid-cols-12">
              
              {/* LEFT PANEL - Engine Config */}
              <div className="lg:col-span-4 bg-[#09090f] border-r border-white/[0.08] p-8 flex flex-col">
                <div className="space-y-1 mb-8">
                  <h3 className="flex items-center gap-2 text-lg font-bold text-white tracking-tight">
                    <span className="text-violet-400 text-xl">⚡</span> Engine Config
                  </h3>
                  <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Configure your API integrations here.</p>
                </div>

                {/* API KEY INPUT */}
                <div className="space-y-3 mb-8">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-semibold text-slate-300">Gemini API Key</label>
                    <div className="group relative cursor-pointer">
                      <HelpCircle size={14} className="text-slate-500" />
                      <div className="absolute bottom-full right-0 mb-2 w-48 bg-black border border-white/10 p-2 rounded-md text-[10px] text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-20 leading-normal">
                        Required to execute language model analysis steps. Stored ONLY locally in browser runtime.
                      </div>
                    </div>
                  </div>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-3 flex items-center text-slate-500"><Key size={16} /></div>
                    <input 
                      type={showApi ? "text" : "password"}
                      className="w-full h-11 bg-white/[0.02] border border-white/10 focus:border-violet-500/50 rounded-[10px] pl-10 pr-10 text-sm text-white focus:outline-none transition-colors focus:ring-1 focus:ring-violet-500/20"
                      placeholder="Enter secret key"
                    />
                    <button onClick={() => setShowApi(!showApi)} className="absolute inset-y-0 right-3 flex items-center text-slate-500 hover:text-white transition-colors">
                      {showApi ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>

                <hr className="border-white/[0.06] mb-8" />

                {/* TALENT POOL INDEX */}
                <div className="space-y-4 mb-8 flex-1">
                  <h4 className="text-sm font-bold text-white flex items-center gap-2">
                    <Layers size={16} className="text-violet-400" /> Talent Pool Index
                  </h4>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    The vector store was pre-cached. <br />
                    Active Entries: <span className="font-bold text-violet-400 bg-violet-400/10 px-1.5 py-0.5 rounded text-[10px]">Indexed Resumes</span>
                  </p>
                </div>

                {/* INFO CALLOUT */}
                <div className="bg-violet-500/5 border border-violet-500/20 rounded-xl p-4 flex gap-3">
                  <Info size={16} className="text-violet-400 shrink-0 mt-0.5" />
                  <p className="text-xs font-medium text-violet-200/70 leading-relaxed">
                    <strong className="text-violet-300">💡 Tip:</strong> If no resumes are uploaded, the system intelligently falls back to the internal talent pool search.
                  </p>
                </div>
              </div>

              {/* MAIN PANEL - Upload */}
              <div className="lg:col-span-8 p-8 sm:p-12 flex flex-col">
                <div className="mb-8">
                  <h3 className="flex items-center gap-3 text-2xl font-bold text-white font-['Space_Grotesk']">
                    <span className="text-2xl">📨</span> Upload Submissions
                  </h3>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
                  
                  {/* Card 1 */}
                  <div className="group border border-dashed border-white/10 bg-white/[0.02] rounded-[16px] p-6 flex flex-col items-center text-center gap-4 hover:bg-white/[0.04] hover:border-violet-500/30 transition-all cursor-pointer aspect-square justify-center">
                    <div className="w-12 h-12 rounded-xl bg-white/[0.03] border border-white/10 flex items-center justify-center group-hover:scale-110 transition-transform text-violet-400">
                      <FileText size={22} />
                    </div>
                    <div>
                      <div className="text-sm font-bold text-white">Job Description</div>
                      <div className="text-[11px] text-slate-500 mt-1 font-medium">.TXT up to 200MB</div>
                    </div>
                  </div>

                  {/* Card 2 */}
                  <div className="relative border border-dashed border-white/10 bg-white/[0.02] rounded-[16px] p-5 flex flex-col justify-between gap-3 min-h-[160px]">
                    <div className="flex items-center gap-3 text-violet-400">
                      <div className="w-8 h-8 rounded-lg bg-white/[0.03] flex items-center justify-center border border-white/10">
                        <UploadCloud size={16} />
                      </div>
                      <div className="text-sm font-bold text-white">Resumes</div>
                    </div>
                    
                    {/* File Chip Component */}
                    <div className="space-y-2">
                      {resumeFiles.map((f, idx) => (
                        <div key={idx} className="flex items-center justify-between px-3 py-2 rounded-lg bg-white/[0.04] border border-white/5 text-[11px] font-medium text-slate-300">
                          <span className="truncate max-w-[100px]">{f.name}</span>
                          <div className="flex items-center gap-2">
                            <span className="text-slate-500 text-[10px]">{f.size}</span>
                            <button onClick={() => removeFile(f.name)} className="text-slate-500 hover:text-red-400"><Plus className="rotate-45" size={14} /></button>
                          </div>
                        </div>
                      ))}
                      <div className="flex items-center justify-center border border-dashed border-white/10 rounded-lg p-2 text-[10px] font-bold text-slate-500 hover:text-white hover:border-white/30 transition-all cursor-pointer uppercase tracking-wider">
                        Add Files
                      </div>
                    </div>
                    <div className="text-[10px] text-slate-600 font-medium text-center">PDFs up to 200MB</div>
                  </div>

                  {/* Card 3 */}
                  <div className="group border border-dashed border-white/10 bg-white/[0.02] rounded-[16px] p-6 flex flex-col items-center text-center gap-4 hover:bg-white/[0.04] hover:border-fuchsia-500/30 transition-all cursor-pointer aspect-square justify-center">
                    <div className="w-12 h-12 rounded-xl bg-white/[0.03] border border-white/10 flex items-center justify-center group-hover:scale-110 transition-transform text-fuchsia-400">
                      <Users size={22} />
                    </div>
                    <div>
                      <div className="text-sm font-bold text-white">LinkedIn Data</div>
                      <div className="text-[11px] text-slate-500 mt-1 font-medium">.JSON up to 200MB</div>
                    </div>
                  </div>

                </div>

                {/* Main Trigger CTA */}
                <div className="flex flex-col items-center gap-4 mt-auto">
                  <button className="w-full max-w-md flex items-center justify-center gap-2 h-14 rounded-[12px] bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-bold text-base shadow-[0_0_30px_rgba(124,58,237,0.25)] hover:shadow-[0_0_40px_rgba(124,58,237,0.45)] transition-all hover:-translate-y-0.5 active:translate-y-0">
                    <Rocket size={18} /> 🚀 Analyze & Rank Talent
                  </button>
                  <p className="text-[11px] font-medium text-slate-500 text-center">Execution involves full iterative graph logic and parsing routines.</p>
                </div>

              </div>
            </div>
          </div>
        </section>

      </main>

      {/* 6) FOOTER */}
      <footer className="bg-[#07070c] border-t border-white/[0.04] pt-20 pb-10 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-10">
          
          {/* Footer Brand */}
          <div className="col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-7 h-7 bg-gradient-to-br from-violet-600 to-indigo-600 rounded flex items-center justify-center text-white">
                <Brain size={15} />
              </div>
              <span className="font-bold font-['Space_Grotesk'] text-white text-lg tracking-tight">NexHire AI</span>
            </div>
            <p className="text-sm text-slate-500 max-w-[240px] leading-relaxed font-medium">
              Deep semantic automation for standard-setting human resources workflows.
            </p>
          </div>

          {/* Footer Nav Grids */}
          <div>
            <h5 className="text-white font-semibold text-sm mb-4 tracking-wide uppercase text-[11px]">Product</h5>
            <ul className="space-y-3 text-slate-400 text-sm font-medium">
              <li><a href="#" className="hover:text-white transition-colors">Agent Platform</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Vector Indices</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
            </ul>
          </div>

          <div>
            <h5 className="text-white font-semibold text-sm mb-4 tracking-wide uppercase text-[11px]">Resources</h5>
            <ul className="space-y-3 text-slate-400 text-sm font-medium">
              <li><a href="#" className="hover:text-white transition-colors">API Docs</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Changelog</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Community</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Case Studies</a></li>
            </ul>
          </div>

          <div>
            <h5 className="text-white font-semibold text-sm mb-4 tracking-wide uppercase text-[11px]">Company</h5>
            <ul className="space-y-3 text-slate-400 text-sm font-medium">
              <li><a href="#" className="hover:text-white transition-colors">About</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>

          <div>
            <h5 className="text-white font-semibold text-sm mb-4 tracking-wide uppercase text-[11px]">Legal</h5>
            <ul className="space-y-3 text-slate-400 text-sm font-medium">
              <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Compliance</a></li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 pt-16 mt-16 border-t border-white/[0.04] flex flex-col sm:flex-row justify-between items-center text-xs text-slate-600 font-medium">
          <p>© {new Date().getFullYear()} NexHire AI. All rights reserved.</p>
          <div className="flex gap-6 mt-4 sm:mt-0">
            <a href="#" className="hover:text-slate-400">Twitter</a>
            <a href="#" className="hover:text-slate-400">GitHub</a>
            <a href="#" className="hover:text-slate-400">LinkedIn</a>
          </div>
        </div>
      </footer>

    </div>
  );
}
