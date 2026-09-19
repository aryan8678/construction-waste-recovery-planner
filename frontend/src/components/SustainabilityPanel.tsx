import React from 'react';
import { Leaf, Info, ShieldAlert, Sparkles, TrendingUp, CheckCircle } from 'lucide-react';
import { SustainabilityAssessment } from '../types';

interface SustainabilityPanelProps {
  sustainability: SustainabilityAssessment;
}

export const SustainabilityPanel: React.FC<SustainabilityPanelProps> = ({ sustainability }) => {
  const indicators = [
    {
      title: 'Landfill Avoidance',
      value: sustainability.landfill_avoidance,
      desc: 'Diverts bulky construction rubble from regional landfill volume.',
      color: 'emerald',
    },
    {
      title: 'Material Recovery',
      value: sustainability.material_recovery,
      desc: 'Fraction of raw mineral/metal/fiber value preserved.',
      color: 'blue',
    },
    {
      title: 'Resource Conservation',
      value: sustainability.resource_conservation,
      desc: 'Reduces demand for virgin rock quarrying or timber harvesting.',
      color: 'teal',
    },
    {
      title: 'Circularity Potential',
      value: sustainability.circularity_potential,
      desc: 'Keeps materials in technical circular closed/open loops.',
      color: 'indigo',
    },
  ];

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4 mb-5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Leaf className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 leading-none">
              Qualitative Sustainability Panel
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Indicative assessment for prototype demonstration
            </p>
          </div>
        </div>

        <span className="text-[11px] font-medium text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full flex items-center gap-1.5 self-start sm:self-auto">
          <Info className="w-3.5 h-3.5 text-slate-400" />
          <span>Non-Numerical Heuristic Scoring</span>
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        {indicators.map((ind, i) => (
          <div
            key={i}
            className="p-4 rounded-lg bg-slate-50 border border-slate-200/80 flex flex-col justify-between"
          >
            <div>
              <span className="text-xs font-medium text-slate-500 block mb-1">
                {ind.title}
              </span>
              <span className="text-sm font-bold text-slate-900 leading-tight block">
                {ind.value}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-3 border-t border-slate-200/50 pt-2 leading-tight">
              {ind.desc}
            </p>
          </div>
        ))}
      </div>

      <div className="bg-amber-50/70 border border-amber-200 rounded-lg p-3 text-[11px] text-amber-900 flex items-start gap-2">
        <ShieldAlert className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Academic Assessment Notice:</span> These indicators represent qualitative circular economy principles aligned with waste hierarchy heuristics. They are not measured numerical life-cycle assessments (LCA) or certified carbon-accounting offsets.
        </div>
      </div>
    </div>
  );
};
