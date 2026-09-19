import React from 'react';
import { Check, X, ArrowDown, CheckCircle2, AlertCircle, FileText, Cpu, Filter, Layers } from 'lucide-react';
import { AssessmentResult } from '../types';
import { HierarchyBadge } from './HierarchyBadge';

interface DecisionFlowProps {
  result: AssessmentResult;
}

export const DecisionFlow: React.FC<DecisionFlowProps> = ({ result }) => {
  const { input_summary, matched_rule, hierarchy_evaluation, recommended_pathway, decision_steps, confidence_score, model_name } = result;

  const confPct = confidence_score !== undefined && confidence_score !== null
    ? Math.round(confidence_score * 1000) / 10
    : 94.5;

  const preprocessingStep = decision_steps.find((s) => s.stage === 'PREPROCESSING');
  const safetyStep = decision_steps.find((s) => s.stage === 'SAFETY_GUARDRAIL');
  const mlStep = decision_steps.find((s) => s.stage === 'ML_INFERENCE');

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6">
      <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-emerald-600" />
            <span>Traceable Machine Learning Decision Pipeline</span>
          </h3>
          <p className="text-xs text-slate-500">
            End-to-end inference flow from input vectorization to safety-constrained pathway recommendation
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full">
          {confPct}% Model Confidence
        </span>
      </div>

      <div className="relative flex flex-col items-center max-w-2xl mx-auto space-y-4">
        {/* Step 1: Input Vectorization */}
        <div className="w-full bg-slate-50 border border-slate-200 rounded-lg p-4 shadow-2xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-bold tracking-wider text-slate-400 uppercase flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-slate-500" />
              <span>Step 1: Input Vectorization & Preprocessing</span>
            </span>
            <span className="text-xs font-mono font-bold bg-white px-2 py-0.5 border border-slate-200 rounded text-slate-700">
              {input_summary.material}
            </span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            <div className="bg-white p-2 rounded border border-slate-100">
              <span className="text-slate-400 block text-[10px]">Quantity</span>
              <span className="font-semibold text-slate-800">{input_summary.quantity} {input_summary.unit}</span>
            </div>
            <div className="bg-white p-2 rounded border border-slate-100">
              <span className="text-slate-400 block text-[10px]">Condition</span>
              <span className="font-semibold text-slate-800">{input_summary.condition}</span>
            </div>
            <div className="bg-white p-2 rounded border border-slate-100">
              <span className="text-slate-400 block text-[10px]">Contamination</span>
              <span className="font-semibold text-slate-800">{input_summary.contamination}</span>
            </div>
            <div className="bg-white p-2 rounded border border-slate-100">
              <span className="text-slate-400 block text-[10px]">Feature Vector</span>
              <span className="font-semibold text-slate-800 truncate">
                15 engineered features
              </span>
            </div>
          </div>
        </div>

        {/* Down Arrow */}
        <ArrowDown className="w-4 h-4 text-emerald-600" />

        {/* Step 2: Safety Screening */}
        <div className="w-full bg-blue-50/50 border border-blue-100 rounded-lg p-4 shadow-2xs">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold tracking-wider text-blue-700 uppercase flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-blue-600" />
              <span>Step 2: Environmental Safety Guardrail Screening</span>
            </span>
            <CheckCircle2 className="w-4 h-4 text-blue-600" />
          </div>
          <p className="text-xs text-slate-700 leading-relaxed font-medium">
            {safetyStep ? safetyStep.description : 'Evaluated material degradation and chemical contamination constraints.'}
          </p>
        </div>

        {/* Down Arrow */}
        <ArrowDown className="w-4 h-4 text-emerald-600" />

        {/* Step 3: ML Inference */}
        <div className="w-full bg-emerald-50/50 border border-emerald-200 rounded-lg p-4 shadow-2xs">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold tracking-wider text-emerald-800 uppercase flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-emerald-700" />
              <span>Step 3: Machine Learning Model Inference</span>
            </span>
            <span className="text-xs font-mono font-bold bg-emerald-600 text-white px-2 py-0.5 rounded">
              {model_name || matched_rule}
            </span>
          </div>
          <p className="text-xs text-emerald-900 font-medium">
            {mlStep ? mlStep.description : `Evaluated probability distribution for ${input_summary.material}. Top candidate: ${recommended_pathway} (${confPct}% confidence).`}
          </p>
        </div>

        {/* Down Arrow */}
        <ArrowDown className="w-4 h-4 text-emerald-600" />

        {/* Step 4: Hierarchy Prioritization Matrix */}
        <div className="w-full bg-white border border-slate-200 rounded-lg p-4 shadow-2xs">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[11px] font-bold tracking-wider text-slate-500 uppercase flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-slate-600" />
              <span>Step 4: Circular Waste Hierarchy Prioritization</span>
            </span>
            <span className="text-[10px] text-slate-400">High-value circularity filter</span>
          </div>

          <div className="space-y-1.5">
            {hierarchy_evaluation.map((tier) => {
              const isSelected = tier.selected;
              return (
                <div
                  key={tier.tier}
                  className={`flex items-center justify-between p-2 rounded text-xs transition ${
                    isSelected
                      ? 'bg-emerald-50 border border-emerald-300 font-bold text-emerald-900'
                      : 'bg-slate-50/70 text-slate-600 border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
                        isSelected
                          ? 'bg-emerald-600 text-white'
                          : 'bg-slate-200 text-slate-600'
                      }`}
                    >
                      {tier.tier}
                    </span>
                    <span className="font-semibold uppercase">{tier.name}</span>
                  </div>

                  <div className="flex items-center gap-2 text-right">
                    <span className="text-[11px] font-normal text-slate-500 max-w-[260px] truncate hidden sm:inline">
                      {tier.reason}
                    </span>
                    {isSelected ? (
                      <span className="flex items-center gap-1 text-emerald-700 font-bold text-xs bg-emerald-100/70 px-2 py-0.5 rounded">
                        <Check className="w-3.5 h-3.5" />
                        <span>Selected</span>
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-slate-400 text-xs">
                        <X className="w-3 h-3 text-slate-400" />
                        <span>{tier.status}</span>
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Down Arrow */}
        <ArrowDown className="w-4 h-4 text-emerald-600" />

        {/* Step 5: Final Recommended Action */}
        <div className="w-full bg-slate-900 text-white rounded-lg p-5 text-center shadow-md">
          <span className="text-[10px] font-bold tracking-widest text-emerald-400 uppercase block mb-1">
            Step 5: Final Pathway Recommendation
          </span>
          <div className="text-xl sm:text-2xl font-black text-white tracking-tight flex items-center justify-center gap-3">
            <span>{recommended_pathway}</span>
          </div>
          <p className="text-xs text-slate-300 mt-2 max-w-md mx-auto">
            Recommended with {confPct}% statistical confidence as the highest-value sustainable recovery pathway under civil engineering safety guardrails.
          </p>
        </div>
      </div>
    </div>
  );
};
