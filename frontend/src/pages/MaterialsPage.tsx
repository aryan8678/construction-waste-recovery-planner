import React, { useState, useEffect } from 'react';
import {
  Recycle,
  Search,
  CheckCircle2,
  AlertTriangle,
  Building2,
  Layers,
  ArrowRight,
} from 'lucide-react';
import { MaterialResponse } from '../types';
import { api } from '../services/api';

export const MaterialsPage: React.FC = () => {
  const [materials, setMaterials] = useState<MaterialResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedMaterial, setSelectedMaterial] = useState<MaterialResponse | null>(null);

  useEffect(() => {
    loadMaterials();
  }, []);

  const loadMaterials = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getMaterials();
      setMaterials(data);
      if (data.length > 0) {
        setSelectedMaterial(data[0]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load materials knowledge base');
    } finally {
      setLoading(false);
    }
  };

  const filtered = materials.filter((m) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return (
      m.name.toLowerCase().includes(term) ||
      m.description.toLowerCase().includes(term) ||
      m.category.toLowerCase().includes(term) ||
      m.typical_waste_source.toLowerCase().includes(term)
    );
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Recycle className="w-6 h-6 text-emerald-600" />
            <span>Materials Knowledge Base</span>
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Technical characteristics, circularity potentials, and handling constraints across 11 key construction fractions
          </p>
        </div>
        <div className="text-xs font-semibold px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full self-start sm:self-auto">
          {materials.length} Materials Documented
        </div>
      </div>

      {/* Search Bar */}
      <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search material characteristics, sources, or recycling potential..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white"
          />
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded-lg text-xs border border-red-200">
          {error}
        </div>
      )}

      {/* Grid of Material Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {loading ? (
          <div className="col-span-3 text-center py-12 text-slate-400">
            Loading materials knowledge base...
          </div>
        ) : filtered.length > 0 ? (
          filtered.map((mat) => (
            <div
              key={mat.name}
              className="bg-white rounded-xl border border-slate-200 shadow-2xs hover:shadow-md hover:border-emerald-300 transition p-5 flex flex-col justify-between space-y-4"
            >
              <div>
                {/* Header */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">{mat.name}</h3>
                    <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200/60">
                      {mat.category}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed mb-4">
                  {mat.description}
                </p>

                {/* Characteristics Box */}
                <div className="space-y-2.5 text-xs">
                  <div>
                    <span className="font-bold text-slate-700 block text-[11px]">
                      Typical Waste Source:
                    </span>
                    <p className="text-slate-600 leading-tight mt-0.5">
                      {mat.typical_waste_source}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                    <div>
                      <span className="font-bold text-slate-700 block text-[10px] uppercase">
                        Reuse Potential
                      </span>
                      <span className="text-[11px] font-semibold text-emerald-700 block">
                        {mat.reuse_potential}
                      </span>
                    </div>
                    <div>
                      <span className="font-bold text-slate-700 block text-[10px] uppercase">
                        Recycling Potential
                      </span>
                      <span className="text-[11px] font-semibold text-blue-700 block">
                        {mat.recycling_potential}
                      </span>
                    </div>
                  </div>

                  {/* Common Applications */}
                  <div>
                    <span className="font-bold text-slate-700 block text-[11px] mb-1">
                      Common Circular Applications:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {mat.common_applications.map((app, i) => (
                        <span
                          key={i}
                          className="text-[10px] font-medium bg-slate-100 text-slate-700 px-2 py-0.5 rounded"
                        >
                          {app}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Considerations */}
                  <div className="pt-2 border-t border-slate-100">
                    <span className="font-bold text-amber-800 flex items-center gap-1 text-[11px] mb-0.5">
                      <AlertTriangle className="w-3 h-3 text-amber-600 shrink-0" />
                      <span>Important Considerations:</span>
                    </span>
                    <p className="text-[11px] text-slate-600 leading-tight">
                      {mat.important_considerations}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-3 text-center py-12 text-slate-400">
            No materials found matching "{searchTerm}".
          </div>
        )}
      </div>
    </div>
  );
};
