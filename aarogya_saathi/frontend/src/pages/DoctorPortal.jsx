import React, { useState } from 'react';
import { Activity, Lock, User, Phone, FileText, AlertTriangle, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const DoctorPortal = () => {
    const [step, setStep] = useState('login'); // 'login', 'otp', 'dashboard'
    const [phone, setPhone] = useState('');

    // Mock Data for the Demo
    const patientData = {
        name: "Shanti Devi",
        age: 60,
        id: "P-9021",
        condition: "Type 2 Diabetes",
        lastVitals: { sugar: "142 mg/dL", bp: "130/85", heartRate: "72 bpm" },
        riskLevel: "Moderate",
        alerts: [
            { time: "10:30 AM", type: "Reflex Trigger", msg: "Patient reported 'Chakkar' (Dizziness)" },
            { time: "10:31 AM", type: "MedPrompt Analysis", msg: "Hypoglycemia Risk detected. Advised Sugar intake." }
        ]
    };

    const handleLogin = (e) => {
        e.preventDefault();
        setStep('otp');
    };

    const handleVerify = (e) => {
        e.preventDefault();
        setStep('dashboard');
    };

    if (step === 'login' || step === 'otp') {
        return (
            <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 font-sans text-slate-900">
                <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
                    <div className="bg-green-700 p-6 text-center">
                        <div className="mx-auto w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-white mb-3">
                            <Activity size={24} />
                        </div>
                        <h1 className="text-2xl font-bold text-white">Aarogya Provider</h1>
                        <p className="text-green-100 text-sm">Secure Clinical Access Portal</p>
                    </div>

                    <div className="p-8">
                        {step === 'login' ? (
                            <form onSubmit={handleLogin} className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">Patient Phone Number</label>
                                    <div className="relative">
                                        <Phone className="absolute left-3 top-3 text-slate-400 w-5 h-5" />
                                        <input
                                            type="tel"
                                            placeholder="+91 98765 43210"
                                            className="w-full pl-10 pr-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-green-500 outline-none transition-all"
                                            value={phone}
                                            onChange={(e) => setPhone(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>
                                <button type="submit" className="w-full bg-slate-900 hover:bg-slate-800 text-white py-3 rounded-lg font-medium transition-colors">
                                    Send Secure OTP
                                </button>
                            </form>
                        ) : (
                            <form onSubmit={handleVerify} className="space-y-6 animate-fadeIn">
                                <div className="text-center mb-6">
                                    <div className="w-12 h-12 bg-green-100 text-green-700 rounded-full flex items-center justify-center mx-auto mb-2">
                                        <Lock size={20} />
                                    </div>
                                    <p className="text-slate-600">Enter the code sent to <br /><span className="font-bold text-slate-900">{phone}</span></p>
                                </div>
                                <div className="flex gap-3 justify-center">
                                    {[1, 2, 3, 4].map((_, i) => (
                                        <input key={i} type="text" maxLength="1" className="w-12 h-14 text-center text-2xl font-bold border border-slate-300 rounded-lg focus:border-green-500 focus:ring-2 focus:ring-green-200 outline-none" />
                                    ))}
                                </div>
                                <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium transition-colors">
                                    Verify & Access Records
                                </button>
                                <button onClick={() => setStep('login')} className="w-full text-slate-500 text-sm hover:text-slate-700">Change Number</button>
                            </form>
                        )}
                    </div>
                </div>
                <Link to="/" className="mt-8 text-slate-400 hover:text-slate-600 text-sm">← Back to Home</Link>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
            {/* Navbar */}
            <nav className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center sticky top-0 z-10">
                <div className="flex items-center gap-2 text-green-700 font-bold text-xl">
                    <Activity /> Aarogya <span className="text-slate-400 font-normal text-sm ml-2">| Provider Portal</span>
                </div>
                <div className="flex items-center gap-4">
                    <div className="text-right hidden md:block">
                        <p className="text-sm font-bold">Dr. Aditi Verma</p>
                        <p className="text-xs text-slate-500">General Physician</p>
                    </div>
                    <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center text-slate-500">
                        <User size={20} />
                    </div>
                </div>
            </nav>

            <main className="container mx-auto px-6 py-8">
                {/* Patient Header */}
                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                    <div className="flex items-center gap-6">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center text-3xl font-bold text-green-700">
                            SD
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-slate-900">{patientData.name}</h1>
                            <p className="text-slate-500">Female, {patientData.age} yrs • ID: {patientData.id}</p>
                            <div className="mt-2 inline-flex items-center gap-2 bg-yellow-50 text-yellow-700 px-3 py-1 rounded-full text-xs font-bold border border-yellow-200">
                                <AlertTriangle size={12} /> High Risk Alert (Today)
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-3">
                        <button className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors">Call Patient</button>
                        <button className="border border-slate-300 text-slate-700 px-6 py-2 rounded-lg font-medium hover:bg-slate-50 transition-colors">Full History</button>
                    </div>
                </div>

                {/* Vitals Grid */}
                <div className="grid md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <p className="text-sm text-slate-500 mb-1">Est. Blood Glucose</p>
                        <p className="text-3xl font-bold text-slate-900">{patientData.lastVitals.sugar}</p>
                        <p className="text-xs text-red-500 mt-2">↑ 12% vs last week</p>
                    </div>
                    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <p className="text-sm text-slate-500 mb-1">Blood Pressure</p>
                        <p className="text-3xl font-bold text-slate-900">{patientData.lastVitals.bp}</p>
                        <p className="text-xs text-green-600 mt-2"><CheckCircle size={10} className="inline" /> Stable</p>
                    </div>
                    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <p className="text-sm text-slate-500 mb-1">Medication Adherence</p>
                        <p className="text-3xl font-bold text-slate-900">85%</p>
                        <p className="text-xs text-orange-500 mt-2">Missed 1 dose yesterday</p>
                    </div>
                </div>

                {/* Live Logs */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="px-6 py-4 border-b border-slate-100 bg-slate-50 flex items-center gap-2">
                        <FileText size={16} className="text-slate-500" />
                        <h3 className="font-bold text-slate-700">Recent Swarm Activity</h3>
                    </div>
                    <div className="divide-y divide-slate-100">
                        {patientData.alerts.map((alert, idx) => (
                            <div key={idx} className="p-4 flex gap-4 hover:bg-slate-50 transition-colors">
                                <div className="text-xs font-mono text-slate-400 whitespace-nowrap pt-1">{alert.time}</div>
                                <div>
                                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 border border-slate-200 px-2 py-0.5 rounded bg-white">{alert.type}</span>
                                    <p className="text-slate-700 mt-1">{alert.msg}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default DoctorPortal;